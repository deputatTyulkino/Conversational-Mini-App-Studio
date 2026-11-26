import json

from app.application.services.tool_router.constants import NONE_CLASS
from app.application.services.tool_router.tool_router_service import normalize_text
from scripts.eval_router import CORPUS_DIR, read_jsonl, split_by_groups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def build_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("tf-idf", TfidfVectorizer(ngram_range=(1, 2))),
            ("classifier", LogisticRegression(max_iter=1000)),
        ]
    )


def main() -> None:
    rows = read_jsonl(CORPUS_DIR / "dev.jsonl")
    groups = json.loads((CORPUS_DIR / "groups.json").read_text(encoding="utf-8"))

    tune, _ = split_by_groups(rows, groups)
    train_rows = [row for row in tune if row["label"] != "ASK"]

    texts = [normalize_text(row["text"]) for row in train_rows]
    labels = [
        NONE_CLASS if row["label"] == "NONE" else row["label"] for row in train_rows
    ]
    model = build_pipeline()
    model.fit(texts, labels)
    print(
        f"Обучено на {len(train_rows)} запросах tune. Классы: {', '.join(model.classes_)}"
    )


if __name__ == "__main__":
    main()
