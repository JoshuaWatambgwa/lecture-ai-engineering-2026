
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from app import tools


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


root_agent = Agent(
    name="aie2026_learning_agent",
    model="gemini-3.5-flash-lite",
    description="AIE2026 learning support agent",
    instruction=INSTRUCTIONS,
    tools=[
        tools.search_glossary,
        tools.get_lecture_summary,
        tools.make_quiz,
        FunctionTool(
            tools.save_learning_log,
            require_confirmation=True,
        ),
    ],
)
