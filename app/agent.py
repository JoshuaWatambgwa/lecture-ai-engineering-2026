
"""第3回: Pydantic AI で作る学習支援エージェント。

使い方:
    uv run python -m app.agent "AIE2026の講座で使う「lecNN-start タグ」とは何ですか？"
    uv run python -m app.agent --trace "LoRAとQLoRAの違いは？"
    uv run python -m app.agent --mcp --trace "LoRAとは？"
    uv run python -m app.agent --mcp --list-tools

エージェント = モデル + ループ + ツール。
モデルは tools.py の関数を「ツール」として呼び出し、その結果を見て回答を作る。
"""

import argparse
import inspect
import json
from pathlib import Path

from pydantic_ai import Agent, DeferredToolRequests
from pydantic_ai.exceptions import ModelHTTPError
from fastmcp import Client
from pydantic_ai.mcp import MCPToolset, StdioTransport
from pydantic_ai.messages import ToolCallPart, ToolReturnPart
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.test import TestModel
from pydantic_ai.providers.google import GoogleProvider

from app import tools
from app.config import MODEL, api_error_message, get_api_key


INSTRUCTIONS = """\
あなたはAIE2026の学習支援エージェントです。利用者の言語で、簡潔に回答してください。

- 講座用語の意味や事実を尋ねられたら、search_glossary で確認してから答える。複数の用語を比較するときは、用語ごとに検索する。
- 講義の内容を尋ねられたら、get_lecture_summary で該当する回を確認する。
- 特定の回の復習問題やクイズを求められたら、make_quiz をその回の番号で呼び出す。返された定義は根拠として使い、利用者が答えを求めない限り問題文だけを提示する。
- 利用者が学習記録の保存を依頼したら、保存する内容がメッセージに含まれている場合は save_learning_log を呼び出す。
- 学習記録の内容が不明な場合のみ、何を記録するか利用者に尋ねる。
- save_learning_log の実行前の確認は、ツールの承認機能に任せる。会話内で別途確認を求めず、承認が必要な場合は CLI の承認フローに従う。
- 用語集や講義資料に根拠がないことは推測で補わず、その旨を伝える。
- 関連する回が分かる場合は回答に示す。
- 宿題の答えを求められたら、答えそのものではなく考え方のヒントを示す。
"""


# モデルは実行時に渡す（テストではAPIを呼ばない TestModel に差し替えるため）
agent = Agent(
    instructions=INSTRUCTIONS,
    output_type=[str, DeferredToolRequests],
)

agent.tool_plain(tools.search_glossary)
agent.tool_plain(tools.get_lecture_summary)
agent.tool_plain(tools.make_quiz)

# 学習記録の保存にはユーザーの承認が必要
agent.tool_plain(tools.save_learning_log, requires_approval=True)


# 第5回: 使う MCP サーバーの設定ファイル
MCP_CONFIG = Path(__file__).resolve().parent / "mcp_servers.json"


def load_mcp_servers(config_path: Path = MCP_CONFIG) -> list[MCPToolset]:
    """設定ファイル（mcpServers 形式）を読み、サーバーごとに接続を作る。

    - "command" があれば stdio：サーバーをサブプロセスとして起動する
    - "url" があれば Streamable HTTP：起動済みのサーバーに接続する
    ツール名にはサーバー名のプレフィックスを付ける。
    """
    config = json.loads(
        Path(config_path).read_text(encoding="utf-8")
    )["mcpServers"]

    toolsets = []

    for name, spec in config.items():
        if "url" in spec:
            transport = spec["url"]
        else:
            transport = StdioTransport(
                spec["command"],
                spec.get("args", []),
                env=spec.get("env"),
            )

        toolsets.append(
            MCPToolset(Client(transport, mode="legacy")).prefixed(name)
        )

    return toolsets


def build_mcp_agent(config_path: Path = MCP_CONFIG) -> Agent:
    """第5回: MCP サーバーが公開するツールを使うエージェント。"""
    return Agent(
        instructions=INSTRUCTIONS,
        toolsets=load_mcp_servers(config_path),
    )


def build_model() -> GoogleModel:
    return GoogleModel(
        MODEL,
        provider=GoogleProvider(api_key=get_api_key()),
    )


def print_tools(target: Agent) -> None:
    """モデルに見えているツールの一覧を表示する。LLM は呼ばない。"""
    model = TestModel(call_tools=[])

    target.run_sync("ツール一覧", model=model)

    tools_seen = model.last_model_request_parameters.function_tools

    print(f"モデルに見えているツール: {len(tools_seen)} 個")

    for tool in tools_seen:
        print(f"\n[{tool.name}]")
        print(
            "  "
            + inspect.cleandoc(tool.description or "").replace(
                "\n", "\n  "
            )
        )

        params = tool.parameters_json_schema.get("properties", {})
        print(f"  引数: {json.dumps(params, ensure_ascii=False)}")


def print_trace(result) -> None:
    """どのツールが、どの引数で呼ばれ、何を返したかを表示する。"""
    print("\n--- trace ---")

    for message in result.all_messages():
        for part in message.parts:
            if isinstance(part, ToolCallPart):
                print(f"[tool call]   {part.tool_name}({part.args})")

            elif isinstance(part, ToolReturnPart):
                print(
                    f"[tool return] {part.tool_name} -> "
                    f"{str(part.content)[:120]}…"
                )

    print(f"[usage] {result.usage}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="学習支援エージェントに質問する"
    )

    parser.add_argument("question", nargs="?")
    parser.add_argument(
        "--trace",
        action="store_true",
        help="ツール呼び出しを表示する",
    )
    parser.add_argument(
        "--mcp",
        action="store_true",
        help="ツールを MCP サーバーから受け取る",
    )
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="モデルに見えるツール一覧を表示して終了する",
    )

    args = parser.parse_args()

    target = build_mcp_agent() if args.mcp else agent

    if args.list_tools:
        print_tools(target)
        return

    if not args.question:
        parser.error("質問を指定してください")

    print(f"[model] {MODEL}")

    if args.mcp:
        print("[tools] MCP サーバー（app/mcp_servers.json）")

    try:
        result = target.run_sync(
            args.question,
            model=build_model(),
        )

        # 承認が必要なツールが呼び出された場合
        if isinstance(result.output, DeferredToolRequests):

            approvals = {}

            for call in result.output.approvals:
                try:
                    response = input(
                        f"Approve {call.tool_name} "
                        f"with arguments {call.args}? [y/N]: "
                    )
                except EOFError:
                    response = ""

                approvals[call.tool_call_id] = (
                    response.strip().casefold() in {"y", "yes"}
                )

            # 承認結果を Pydantic AI に渡す
            deferred_tool_results = result.output.build_results(
                approvals=approvals
            )

            # 承認結果を使ってエージェントの実行を再開する
            result = target.run_sync(
                message_history=result.all_messages(),
                deferred_tool_results=deferred_tool_results,
                model=build_model(),
            )

    except ModelHTTPError as e:
        print(api_error_message(e.status_code, str(e.body)[:200]))
        raise SystemExit(1)

    print(result.output)

    if args.trace:
        print_trace(result)


if __name__ == "__main__":
    main()
