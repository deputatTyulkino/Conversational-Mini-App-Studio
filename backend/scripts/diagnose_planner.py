"""Диагностика Project Planner по проверочным предсказаниям на tune."""

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from itertools import chain, product
from pathlib import Path
from statistics import median, quantiles
from uuid import uuid4

from app.application.schemas.tool_router.tool_router_schema import (
    RouteCandidate,
    RouteDecision,
    RouterInput,
    RouteStatus,
)
from app.application.services.tool_router.constants import NONE_CLASS
from app.application.services.tool_router.rules import rules_scorer
from app.application.services.tool_router.tool_router_service import (
    MANIFESTS_DIR,
    ToolRouterService,
    build_decision,
    load_app_versions,
    normalize_text,
    rank,
)
from joblib import dump, load
from scripts.eval_router import (
    CORPUS_DIR,
    LABELS,
    MARGIN,
    THRESHOLD,
    format_ratio,
    is_correct,
    read_jsonl,
    short_answer,
    split_by_groups,
)
from scripts.train import build_pipeline
from sklearn.base import clone
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline

PLANNER = "project_planner"
CLASS_WEIGHTS = (None, "balanced")
THRESHOLDS = (0.30, 0.35, 0.40, 0.45, 0.50, 0.55)
MARGINS = (0.02, 0.05, 0.10)
CHAR_ARTIFACT = MANIFESTS_DIR.parent / "data" / "router" / "char_wb_balanced.joblib"
CHAR_OOF_PATH = CHAR_ARTIFACT.with_name("char_wb_balanced_tune_oof.jsonl")
ASK_GAPS = (0.05, 0.10, 0.15)
ASK_NONE_TOLERANCES = (0.00, 0.03, 0.06)


@dataclass
class ThresholdResult:
    threshold: float
    margin: float
    statuses: Counter[RouteStatus]
    correct: int
    planner_opened: int
    planner_predictions: int
    none_opened: int
    ask_correct: int


@dataclass
class AskProbeRow:
    label: str
    p2: float
    app_gap: float
    none_gap: float
    baseline_status: RouteStatus
    baseline_correct: bool
    pair_correct: bool


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--compare-tfidf",
        action="store_true",
        help="сравнить словесные и символьные n-граммы при порогах 0.30 / 0.02",
    )
    mode.add_argument(
        "--tune-char", action="store_true", help="диагностика ASK и подбор порогов"
    )
    mode.add_argument(
        "--restore-char-oof",
        action="store_true",
        help="сохранить прогнозы символьной модели на tune",
    )
    mode.add_argument(
        "--report-char-oof",
        action="store_true",
        help="разобрать ASK по сохранённым прогнозам",
    )
    mode.add_argument(
        "--probe-ask-oof",
        action="store_true",
        help="проверить правило выбора пары по сохранённым прогнозам tune",
    )
    mode.add_argument(
        "--compare-rules-oof",
        action="store_true",
        help="сравнить правила и символьную модель на сохранённых прогнозах tune",
    )
    mode.add_argument(
        "--check-char",
        nargs=2,
        type=float,
        metavar=("THRESHOLD", "MARGIN"),
        help="обучить символьную модель на tune и оценить на check с заранее выбранными порогами",
    )
    args = parser.parse_args()

    rows = read_jsonl(CORPUS_DIR / "dev.jsonl")
    groups = json.loads((CORPUS_DIR / "groups.json").read_text(encoding="utf-8"))
    tune, check = split_by_groups(rows, groups)
    if args.check_char:
        threshold, margin = args.check_char
        fit_and_check_char(tune, check, threshold, margin, CHAR_ARTIFACT)
        return
    if args.restore_char_oof:
        fold_numbers: dict[int, int] = {}
        predictions = out_of_fold_predictions(
            tune, groups, {"char": char_pipeline()}, fold_numbers=fold_numbers
        )
        CHAR_OOF_PATH.parent.mkdir(parents=True, exist_ok=True)
        with CHAR_OOF_PATH.open("w", encoding="utf-8", newline="\n") as file:
            for index, row in enumerate(tune):
                record = {
                    "id": row["id"],
                    "fold": fold_numbers[index],
                    "scores": predictions["char"][index],
                }
                file.write(
                    json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n"
                )
        print(f"Отложенные прогнозы сохранены: {CHAR_OOF_PATH}")
    if args.restore_char_oof or args.report_char_oof:
        report_saved_ask(tune)
        return
    if args.probe_ask_oof:
        probe_ask(tune, load_oof_scores(tune))
        return
    if args.compare_rules_oof:
        compare_rules_oof(tune, groups, load_oof_scores(tune))
        return
    if args.tune_char:
        predictions = out_of_fold_predictions(tune, groups, {"char": char_pipeline()})
        report_char_tuning(tune, predictions["char"])
        return
    if args.compare_tfidf:
        word = build_pipeline().set_params(classifier__class_weight="balanced")
        pipelines = {"word (1, 2)": word, "char_wb (3, 5)": char_pipeline()}
        predictions = out_of_fold_predictions(tune, groups, pipelines)
        report_tfidf(tune, predictions)
    else:
        pipelines = {
            repr(weight): build_pipeline().set_params(classifier__class_weight=weight)
            for weight in CLASS_WEIGHTS
        }
        predictions = out_of_fold_predictions(tune, groups, pipelines)
        report_thresholds(tune, predictions)


def char_pipeline() -> Pipeline:
    return build_pipeline().set_params(
        classifier__class_weight="balanced",
        **{"tf-idf__analyzer": "char_wb", "tf-idf__ngram_range": (3, 5)},
    )


def out_of_fold_predictions(
    tune: list[dict],
    groups: dict[str, str],
    pipelines: dict[str, Pipeline],
    *,
    fold_numbers: dict[int, int] | None = None,
) -> dict[str, dict[int, dict[str, float]]]:
    texts = [normalize_text(row["text"]) for row in tune]
    labels = [row["label"] for row in tune]
    tune_groups = [groups[row["id"]] for row in tune]

    splitter = StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=42)
    predictions: dict[str, dict[int, dict[str, float]]] = {
        name: {} for name in pipelines
    }
    folds = splitter.split(texts, labels, tune_groups)
    for fold, (train_indices, validation_indices) in enumerate(folds, start=1):
        if fold_numbers is not None:
            fold_numbers.update((int(index), fold) for index in validation_indices)
        fit_indices = [index for index in train_indices if labels[index] != "ASK"]
        train_labels = [
            NONE_CLASS if labels[index] == "NONE" else labels[index]
            for index in fit_indices
        ]
        train_texts = [texts[index] for index in fit_indices]
        validation_texts = [texts[index] for index in validation_indices]
        for name, pipeline in pipelines.items():
            variant_predictions = predictions[name]
            model = clone(pipeline)
            model.fit(train_texts, train_labels)
            probabilities = model.predict_proba(validation_texts)
            for index, scores in zip(validation_indices, probabilities, strict=True):
                if index in variant_predictions:
                    raise RuntimeError(
                        f"{name}: повторное предсказание "
                        f"для запроса {tune[index]['id']}"
                    )
                variant_predictions[index] = {
                    str(label): float(score)
                    for label, score in zip(model.classes_, scores, strict=True)
                }

    expected_indices = set(range(len(tune)))
    for name, variant_predictions in predictions.items():
        if variant_predictions.keys() != expected_indices:
            raise RuntimeError(
                f"{name}: предсказания получены не для всех запросов tune"
            )
    return predictions


def load_oof_scores(tune: list[dict]) -> dict[int, dict[str, float]]:
    records = read_jsonl(CHAR_OOF_PATH)
    by_id = {record["id"]: record for record in records}
    if (
        len(records) != 270
        or len(by_id) != 270
        or by_id.keys() != {row["id"] for row in tune}
    ):
        raise RuntimeError("В JSONL должны быть все 270 уникальных запросов tune")
    scores_by_index: dict[int, dict[str, float]] = {
        index: by_id[row["id"]]["scores"] for index, row in enumerate(tune)
    }
    classes = {NONE_CLASS, "research_board", PLANNER, "data_explorer"}
    if any(scores.keys() != classes for scores in scores_by_index.values()):
        raise RuntimeError("Для каждого запроса нужны оценки всех четырёх классов")
    return scores_by_index


def compare_rules_oof(
    tune: list[dict], groups: dict[str, str], predictions: dict[int, dict[str, float]]
) -> None:
    app_versions = load_app_versions(MANIFESTS_DIR)
    rules_router = ToolRouterService(rules_scorer, THRESHOLD, MARGIN, app_versions)
    outcomes = ((True, True), (True, False), (False, True), (False, False))
    by_label: dict[str, Counter[tuple[bool, bool]]] = {
        label: Counter() for label in LABELS
    }
    total: Counter[tuple[bool, bool]] = Counter()
    ml_only: list[tuple[dict, RouteDecision, RouteDecision]] = []
    both_wrong: list[tuple[dict, RouteDecision, RouteDecision]] = []
    for index, row in enumerate(tune):
        rules = rules_router(
            RouterInput(chat_id=uuid4(), project_id=None, text=row["text"])
        )
        ml = build_decision(predictions[index], 0.30, 0.02, app_versions)
        outcome = (is_correct(row, rules), is_correct(row, ml))
        by_label[row["label"]][outcome] += 1
        total[outcome] += 1
        if outcome == (False, True):
            ml_only.append((row, rules, ml))
        elif outcome == (False, False):
            both_wrong.append((row, rules, ml))

    both_right, rules_only, fixed, missed = (total[outcome] for outcome in outcomes)
    rules_correct = both_right + rules_only
    ml_correct = both_right + fixed
    if (total.total(), rules_correct, ml_correct) != (270, 236, 159):
        raise RuntimeError(
            f"Не совпали контрольные итоги: всего {total.total()}, "
            f"правила {rules_correct}, ML {ml_correct}"
        )

    print(
        "Эталон | Обе системы правы | Правы только правила | Права только ML | Обе ошиблись"
    )
    for label, counts in chain(by_label.items(), [("Итого", total)]):
        print(f"{label} | " + " | ".join(str(counts[outcome]) for outcome in outcomes))
    print(
        f"Из {fixed + missed} ошибок правил модель исправляет {fixed}, обе системы ошибаются в {missed} случаях."
    )
    print(
        f"Теоретический потолок на tune: {format_ratio(rules_correct + fixed, len(tune))}"
    )

    print_comparison_examples("Права только ML", ml_only, groups)
    print_comparison_examples("Обе ошиблись", both_wrong, groups)


def print_comparison_examples(
    title: str,
    cases: list[tuple[dict, RouteDecision, RouteDecision]],
    groups: dict[str, str],
) -> None:
    print(f"\n{title}")
    first_by_label: dict[str, tuple[dict, RouteDecision, RouteDecision]] = {}
    for case in cases:
        first_by_label.setdefault(case[0]["label"], case)
    used_groups: set[str] = set()
    for row, rules, ml in chain(first_by_label.values(), cases):
        group = groups[row["id"]]
        if group in used_groups:
            continue
        used_groups.add(group)
        expected = row["label"]
        if expected == "ASK":
            expected = f"ASK[{'/'.join(row['candidates'])}]"
        print(
            f"{row['id']} | {row['text']} | {expected} | {short_answer(rules)} | {short_answer(ml)}"
        )
        if len(used_groups) == 5:
            break


def report_saved_ask(tune: list[dict]) -> None:
    scores_by_index = load_oof_scores(tune)
    asks = [(index, row) for index, row in enumerate(tune) if row["label"] == "ASK"]
    if len(asks) != 41:
        raise RuntimeError(f"В tune найдено {len(asks)} запросов ASK, ожидался 41")
    result = evaluate(
        tune, scores_by_index, load_app_versions(MANIFESTS_DIR), 0.30, 0.02
    )
    initial_hits = 0
    none_displaced = []
    app_order_errors = []
    for index, row in asks:
        ranked = rank(scores_by_index[index])
        expected = set(row["candidates"])
        apps = [label for label, _ in ranked if label != NONE_CLASS]
        if {label for label, _ in ranked[:2]} == expected:
            initial_hits += 1
        elif set(apps[:2]) == expected:
            none_displaced.append((row, ranked))
        else:
            app_order_errors.append((row, ranked))

    print(
        f"Проверены {len(scores_by_index)} уникальных прогнозов tune, из них ASK: {len(asks)}"
    )
    print(f"Строгая accuracy: {format_ratio(result.correct, len(tune))}")
    print(f"Эталонная пара в общем топ-2: {initial_hits}/{len(asks)}")
    if (result.correct, initial_hits) != (159, 7):
        raise RuntimeError("Контрольные результаты не совпали с 159/270 и 7/41")
    if len(none_displaced) + len(app_order_errors) != 34:
        raise RuntimeError("Ожидалось 34 промаха в общем топ-2")
    print(
        f"K — правильная пара среди приложений: {initial_hits + len(none_displaced)}/41"
    )
    for title, cases in (
        ("none вытеснил приложение", none_displaced),
        ("неверный порядок приложений", app_order_errors),
    ):
        print(f"{title}: {len(cases)}")
        for row, ranked in cases[:3]:
            scores = ", ".join(f"{label}={score!r}" for label, score in ranked)
            pair = " / ".join(row["candidates"])
            print(f"  {row['id']} | {row['text']} | {pair} | {scores}")


def probe_ask(tune: list[dict], predictions: dict[int, dict[str, float]]) -> None:
    app_versions = load_app_versions(MANIFESTS_DIR)
    rows: list[AskProbeRow] = []
    for index, row in enumerate(tune):
        scores = predictions[index]
        apps = [(label, score) for label, score in rank(scores) if label != NONE_CLASS]
        (_, p1), (_, p2) = apps[:2]
        baseline = build_decision(scores, 0.30, 0.02, app_versions)
        offered_pair = RouteDecision(
            status=RouteStatus.AMBIGUOUS,
            confidence=p1,
            margin=p1 - p2,
            candidates=[
                RouteCandidate(app_id=label, score=score) for label, score in apps[:2]
            ],
        )
        rows.append(
            AskProbeRow(
                label=row["label"],
                p2=p2,
                app_gap=p1 - p2,
                none_gap=p2 - scores[NONE_CLASS],
                baseline_status=baseline.status,
                baseline_correct=is_correct(row, baseline),
                pair_correct=is_correct(row, offered_pair),
            )
        )

    print("Медиана [Q1; Q3] по эталонным меткам")
    print("Метка | n | p2 | p1 − p2 | p2 − p_none")
    for label in LABELS:
        group = [row for row in rows if row.label == label]
        summaries = [
            format_quartiles(values)
            for values in (
                [row.p2 for row in group],
                [row.app_gap for row in group],
                [row.none_gap for row in group],
            )
        ]
        print(f"{label} | {len(group)} | " + " | ".join(summaries))

    baseline_correct = sum(row.baseline_correct for row in rows)
    baseline_ask = sum(row.label == "ASK" and row.baseline_correct for row in rows)
    baseline_none = sum(
        row.label == "NONE" and row.baseline_status is RouteStatus.AMBIGUOUS
        for row in rows
    )
    print(f"\nИсходные пороги 0.30/0.02: {format_ratio(baseline_correct, len(rows))}")
    print(
        f"Исходные верные ASK: {baseline_ask}, исходные NONE → ambiguous: {baseline_none}"
    )
    print(
        "d | e | Строгая accuracy | Верные ASK | Новые NONE → ASK | Верные открытия → ASK | Исправлено | Испорчено"
    )
    for d, e in product(ASK_GAPS, ASK_NONE_TOLERANCES):
        correct_ask = none_to_ask = opened_to_ask = fixed = spoiled = 0
        for row in rows:
            offer_pair = row.app_gap <= d and row.none_gap >= -e
            correct = row.pair_correct if offer_pair else row.baseline_correct
            correct_ask += row.label == "ASK" and correct
            fixed += correct and not row.baseline_correct
            spoiled += row.baseline_correct and not correct
            if offer_pair:
                none_to_ask += (
                    row.label == "NONE"
                    and row.baseline_status is not RouteStatus.AMBIGUOUS
                )
                opened_to_ask += (
                    row.baseline_correct and row.baseline_status is RouteStatus.MATCHED
                )
        accuracy = format_ratio(baseline_correct + fixed - spoiled, len(rows))
        print(
            f"{d:.2f} | {e:.2f} | {accuracy} | {correct_ask} | {none_to_ask} | {opened_to_ask} | {fixed} | {spoiled}"
        )


def format_quartiles(values: list[float]) -> str:
    q1, _, q3 = quantiles(values, n=4, method="inclusive")
    return f"{median(values):.3f} [{q1:.3f}; {q3:.3f}]"


def report_tfidf(
    tune: list[dict], predictions: dict[str, dict[int, dict[str, float]]]
) -> None:
    label_counts = Counter(row["label"] for row in tune)
    print("Доля первых мест до применения порогов")
    print("Метка | " + " | ".join(predictions))
    first_places: dict[str, Counter[str]] = {}
    for name, scores_by_index in predictions.items():
        counts: Counter[str] = Counter()
        for index, row in enumerate(tune):
            expected = row["label"]
            model_label = NONE_CLASS if expected == "NONE" else expected
            if expected != "ASK" and rank(scores_by_index[index])[0][0] == model_label:
                counts[expected] += 1
        first_places[name] = counts
    for label in LABELS:
        if label != "ASK":
            ratios = [
                format_ratio(counts[label], label_counts[label])
                for counts in first_places.values()
            ]
            print(f"{label} | " + " | ".join(ratios))

    threshold, margin = 0.30, 0.02
    app_versions = load_app_versions(MANIFESTS_DIR)
    print(f"\nРешения при порогах {threshold:.2f}/{margin:.2f}")
    print(
        "TF-IDF | Строгая accuracy | Планировщик открыт | Precision | Открытия на NONE | Верные ASK"
    )
    for name, scores_by_index in predictions.items():
        result = evaluate(tune, scores_by_index, app_versions, threshold, margin)
        print(f"{name} | {format_metrics(result, label_counts, len(tune))}")


def report_thresholds(
    tune: list[dict], predictions: dict[str, dict[int, dict[str, float]]]
) -> None:
    app_versions = load_app_versions(MANIFESTS_DIR)
    current_results: dict[str, ThresholdResult] = {}
    print(f"Решения при текущих порогах {THRESHOLD:.2f}/{MARGIN:.2f}")
    for weight, variant_predictions in predictions.items():
        current = evaluate(tune, variant_predictions, app_versions, THRESHOLD, MARGIN)
        current_results[weight] = current
        counts = ", ".join(
            f"{status.value}: {current.statuses[status]}" for status in RouteStatus
        )
        print(f"class_weight={weight}: {counts}")

    label_counts = Counter(row["label"] for row in tune)
    print(
        "\nclass_weight | Пороги | Строгая accuracy | Планировщик открыт | "
        "Precision | Открытия на NONE | Верные ASK"
    )
    for weight, variant_predictions in predictions.items():
        current = current_results[weight]
        best = best_thresholds(tune, variant_predictions, app_versions, current)
        for name, result in (("текущие", current), ("лучшие", best)):
            print(
                f"{weight} | {name} {result.threshold:.2f}/{result.margin:.2f} | "
                f"{format_metrics(result, label_counts, len(tune))}"
            )


def best_thresholds(
    tune: list[dict],
    predictions: dict[int, dict[str, float]],
    app_versions: dict[str, str],
    current: ThresholdResult,
) -> ThresholdResult:
    grid_results = (
        current
        if (threshold, margin) == (current.threshold, current.margin)
        else evaluate(tune, predictions, app_versions, threshold, margin)
        for threshold, margin in product(THRESHOLDS, MARGINS)
    )
    return max(grid_results, key=lambda result: (result.correct, -result.none_opened))


def report_char_tuning(
    tune: list[dict], predictions: dict[int, dict[str, float]]
) -> None:
    app_versions = load_app_versions(MANIFESTS_DIR)
    ask_rows = [(index, row) for index, row in enumerate(tune) if row["label"] == "ASK"]
    threshold, margin = 0.30, 0.02
    top_pair = ambiguous = correct_pair = 0
    for index, row in ask_rows:
        scores = predictions[index]
        top_pair += {label for label, _ in rank(scores)[:2]} == set(row["candidates"])
        decision = build_decision(scores, threshold, margin, app_versions)
        ambiguous += decision.status is RouteStatus.AMBIGUOUS
        correct_pair += is_correct(row, decision)

    total = len(ask_rows)
    print(f"ASK при {threshold:.2f}/{margin:.2f}")
    print(f"A — эталонная пара в первых двух классах: {top_pair}/{total}")
    print(f"B — ambiguous с любой парой: {ambiguous}/{total}")
    print(f"C — ambiguous с верной парой: {correct_pair}/{total}")
    print(f"A − C: {top_pair - correct_pair}")
    print(f"{total} − A: {total - top_pair}")

    current = evaluate(tune, predictions, app_versions, threshold, margin)
    best = best_thresholds(tune, predictions, app_versions, current)
    label_counts = Counter(row["label"] for row in tune)
    print(f"Выбранные пороги: {best.threshold:.2f}/{best.margin:.2f}")
    print(
        "Строгая accuracy | Планировщик открыт | Precision | Открытия на NONE | Верные ASK"
    )
    print(format_metrics(best, label_counts, len(tune)))


def fit_and_check_char(
    tune: list[dict],
    check: list[dict],
    threshold: float,
    margin: float,
    artifact_path: Path,
) -> None:
    train_rows = [row for row in tune if row["label"] != "ASK"]
    pipeline = char_pipeline()
    pipeline.fit(
        [normalize_text(row["text"]) for row in train_rows],
        [NONE_CLASS if row["label"] == "NONE" else row["label"] for row in train_rows],
    )
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    dump(
        {"pipeline": pipeline, "threshold": threshold, "margin": margin}, artifact_path
    )
    artifact = load(artifact_path)
    loaded_pipeline = artifact["pipeline"]
    probabilities = loaded_pipeline.predict_proba(
        [normalize_text(row["text"]) for row in check]
    )
    predictions = {
        index: {
            str(label): float(score)
            for label, score in zip(loaded_pipeline.classes_, scores, strict=True)
        }
        for index, scores in enumerate(probabilities)
    }
    result = evaluate(
        check,
        predictions,
        load_app_versions(MANIFESTS_DIR),
        artifact["threshold"],
        artifact["margin"],
    )
    print(f"Обучающих запросов tune: {len(train_rows)}")
    print(f"Артефакт сохранён и загружен: {artifact_path}")
    print(f"Символьная модель на check: {format_ratio(result.correct, len(check))}")


def format_metrics(
    result: ThresholdResult, label_counts: Counter[str], total: int
) -> str:
    precision = (
        f"{result.planner_opened}/{result.planner_predictions}"
        if result.planner_predictions
        else "—"
    )
    return (
        f"{format_ratio(result.correct, total)} | "
        f"{result.planner_opened}/{label_counts[PLANNER]} | {precision} | "
        f"{result.none_opened}/{label_counts['NONE']} | "
        f"{result.ask_correct}/{label_counts['ASK']}"
    )


def evaluate(
    tune: list[dict],
    predictions: dict[int, dict[str, float]],
    app_versions: dict[str, str],
    threshold: float,
    margin: float,
) -> ThresholdResult:
    statuses: Counter[RouteStatus] = Counter()
    correct = planner_opened = planner_predictions = none_opened = ask_correct = 0
    for index, row in enumerate(tune):
        decision = build_decision(predictions[index], threshold, margin, app_versions)
        statuses[decision.status] += 1
        matched = decision.status is RouteStatus.MATCHED
        opened_planner = matched and decision.app_id == PLANNER
        proper_route = is_correct(row, decision)
        label = row["label"]
        correct += proper_route
        planner_predictions += opened_planner
        planner_opened += opened_planner and label == PLANNER
        none_opened += matched and label == "NONE"
        ask_correct += proper_route and label == "ASK"

    return ThresholdResult(
        threshold=threshold,
        margin=margin,
        statuses=statuses,
        correct=correct,
        planner_opened=planner_opened,
        planner_predictions=planner_predictions,
        none_opened=none_opened,
        ask_correct=ask_correct,
    )


if __name__ == "__main__":
    main()
