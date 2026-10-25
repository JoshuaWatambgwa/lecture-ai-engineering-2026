"""第1回: 素のLLMと会話するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 初回の質問を省略すると、講座に固有の質問をする
                                         # 以降は質問を入力。空行で終了。

ツールは使わず、同じ会話の履歴を保って追加の質問ができる「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time

from google import genai
from google.genai.chats import Chat
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# Course-specific question. The correct answer is in the homework-levels entry of data/glossary.json.
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(chat: Chat, question: str) -> str:
    start = time.perf_counter()
    try:
        response = chat.send_message(question)
    except errors.APIError:
        elapsed = time.perf_counter() - start
        print(
            f"[request] elapsed={elapsed:.3f}s, "
            "input_tokens=unavailable, output_tokens=unavailable"
        )
        raise

    elapsed = time.perf_counter() - start
    usage = response.usage_metadata
    if usage is not None:
        print(
            f"[request] elapsed={elapsed:.3f}s, "
            f"input_tokens={usage.prompt_token_count}, "
            f"output_tokens={usage.candidates_token_count}"
        )
    else:
        print(
            f"[request] elapsed={elapsed:.3f}s, "
            "input_tokens=unavailable, output_tokens=unavailable"
        )

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMと会話する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(model=MODEL)
        question = args.question
        while True:
            print(f"[質問] {question}\n")
            print(ask(chat, question))
            question = input("続けて質問してください（空行で終了）: ").strip()
            if not question:
                break
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
