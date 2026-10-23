"""第5回: 用語集と各回の要点を MCP サーバーとして公開する。

使い方:
    uv run python -m app.agent --mcp --list-tools   # このサーバーが公開するツールを一覧する（APIキー不要）
    uv run python -m app.mcp_server --http          # Streamable HTTP で起動する（http://127.0.0.1:8000/mcp）

引数なしで実行すると stdio（標準入出力）で待ち受ける。これは MCP クライアント（app.agent の --mcp や
Copilot Chat）がサブプロセスとして起動する使い方なので、手で実行すると入力待ちのまま止まって見える。

第3回では tools.py の関数を agent.py に直接登録した。MCP サーバーにすると、同じ関数を
Pydantic AI 以外のクライアント（Copilot Chat など）からも、共通の手順で使えるようになる。
"""

import argparse

from mcp.server.mcpserver import MCPServer

from app import tools

# Server name and instructions, displayed to clients (distinct from the "glossary" key in the config file).
server = MCPServer(
    "aie2026-glossary",
    instructions="AIE2026（AIエンジニアリング実践講座）の用語集と各回の要点を提供する。",
)

# Expose the same function from Session 3 as an MCP tool; its docstring and type hints become the description.
server.tool()(tools.search_glossary)

# TODO (Session 5 exercise): Expose tools.get_lecture_summary as well (using the same pattern as the line above).
# If you created make_quiz in Session 3, you can expose that too.


def main() -> None:
    parser = argparse.ArgumentParser(description="用語集 MCP サーバー")
    parser.add_argument("--http", action="store_true", help="Streamable HTTP で起動する（既定は stdio）")
    args = parser.parse_args()
    if args.http:
        print("MCP サーバーを http://127.0.0.1:8000/mcp で起動します（Ctrl+C で停止）")
        server.run(transport="streamable-http")
    else:
        # With stdio, standard output carries the protocol, so do not print to it.
        server.run()


if __name__ == "__main__":
    main()
