"""第3回: エージェントに持たせるツール。

ここに書いた関数の docstring と型ヒントが、そのままモデルへの「ツールの説明文」になる。
説明文を書き換えると、モデルがツールを使うかどうか・どんな引数で呼ぶかが変わる。
"""

import json
import random
from datetime import datetime
from functools import cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LEARNING_LOG_DIR = Path(__file__).resolve().parent.parent / "learning_log"
MAX_RESULTS = 3


@cache
def load_glossary() -> list[dict]:
    with open(DATA_DIR / "glossary.json", encoding="utf-8") as f:
        return json.load(f)["terms"]


def _normalize(text: str) -> str:
    return text.casefold().replace(" ", "").replace("　", "")


def _names(entry: dict) -> list[str]:
    return [_normalize(entry["term"]), _normalize(entry["id"])] + [
        _normalize(a) for a in entry["aliases"]
    ]


def search_glossary(query: str) -> str:
    """講座の用語集から用語を検索し、定義・対象の回・関連用語を返す。

    AIE2026の講義内容やAIエンジニアリング用語について、意味を説明したり比較したり
    するときに使う。query には用語を1つだけ指定する（例: "LoRA"）。
    """
    q = _normalize(query)
    if not q:
        return "検索語が空です。調べたい用語を1つ指定してください。"
    glossary = load_glossary()

    exact = [e for e in glossary if q in _names(e)]
    # 「r」のような短い別名が何にでも当たらないよう、名前側が短いものは除く
    partial = [
        e for e in glossary
        if e not in exact and any(q in n or (len(n) >= 3 and n in q) for n in _names(e))
    ]
    in_definition = [
        e for e in glossary
        if e not in exact and e not in partial and q in _normalize(e["definition"])
    ]
    hits = (exact + partial + in_definition)[:MAX_RESULTS]

    if not hits:
        return f"用語集に「{query}」は見つかりませんでした。"
    return json.dumps(
        [
            {
                "term": e["term"],
                "lecture": e["lecture"],
                "definition": e["definition"],
                "related": e["related"],
            }
            for e in hits
        ],
        ensure_ascii=False,
    )


def get_lecture_summary(lecture: int) -> str:
    """指定した回（1始まりの整数）の講義資料を返す。

    「第N回では何を学ぶ？」など、特定の回の内容や扱う話題を尋ねられたときに使う。
    """
    path = DATA_DIR / "lectures" / f"{lecture:02d}.md"
    if not path.exists():
        available = sorted(p.stem for p in (DATA_DIR / "lectures").glob("*.md"))
        return f"第{lecture}回の要点はまだありません。用意されている回: {', '.join(available)}"
    return path.read_text(encoding="utf-8")



def make_quiz(lecture: int) -> str:
    """指定した回の用語集から復習問題を1問作り、問題と答えを返す。

    学習者が特定の回の復習問題・確認問題・クイズを求めたときに使う。
    lecture には対象の回（1始まりの整数）を指定する。返り値には答えも含まれるため、
    学習者が答えを求めていない場合は問題文だけを提示する。
    """
    terms = [entry for entry in load_glossary() if entry["lecture"] == lecture]
    if not terms:
        return f"第{lecture}回の用語が用語集に見つかりませんでした。"

    entry = random.choice(terms)
    return f"質問:「{entry['term']}」とは何ですか？\n答え:{entry['definition']}"


def save_learning_log(record: str) -> str:
    """学習者の学習記録を learning_log/learning_log.md に追記する。

    学習者から、学んだこと・疑問・進捗などを記録するよう頼まれたときに使う。
    保存は元に戻しにくいため、実行前に必ず本人の承認を得る。
    """
    content = record.strip()
    if not content:
        raise ValueError("保存する学習記録が空です。")

    LEARNING_LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LEARNING_LOG_DIR / "learning_log.md"
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"## {timestamp}\n\n{content}\n\n")

    return f"学習記録を {log_path.relative_to(LEARNING_LOG_DIR.parent)} に保存しました。"
