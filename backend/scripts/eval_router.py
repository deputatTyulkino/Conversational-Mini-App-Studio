"""Проверка точности роутера с правилами на corpus/dev.jsonl.

Запуск из backend/:
    python -m scripts.eval_router                 # точность на части tune
    python -m scripts.eval_router --errors        # + ошибки части tune
    python -m scripts.eval_router --short-stems   # + что находят короткие основы
    python -m scripts.eval_router --check         # + точность на части check

dev делится по группам перефразировок (groups.json): ~80% запросов (tune) —
для подбора слов и форы, ~20% (check) — только для итоговой проверки.
Часть check считается только с флагом --check, и её ошибки не печатаются
никогда, чтобы не подгонять под неё правила. test.jsonl не используется.
"""

import argparse
import json
import random
import re
from collections import Counter
from pathlib import Path
from uuid import uuid4

from app.application.schemas.tool_router.tool_router_schema import (
    RouteDecision,
    RouterInput,
    RouteStatus,
)
from app.application.services.tool_router.rules import STEMS, rules_scorer
from app.application.services.tool_router.tool_router_service import (
    MANIFESTS_DIR,
    ToolRouterService,
    load_app_versions,
    normalize_text,
)

CORPUS_DIR = Path(__file__).resolve().parents[2] / "corpus"

THRESHOLD = 0.55
MARGIN = 0.10

CHECK_SHARE = 0.2
SEED = 42


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def split_by_groups(rows: list[dict], groups: dict[str, str]) -> tuple[list, list]:
    # Группа целиком попадает в одну часть (перефразировки не разрезаем).
    # Делим отдельно внутри каждой метки, чтобы в check были все метки:
    # группы очень разного размера (от 1 до 32 запросов).
    rng = random.Random(SEED)
    check_names: set[str] = set()
    for label in sorted({row["label"] for row in rows}):
        label_rows = [row for row in rows if row["label"] == label]
        sizes = Counter(groups[row["id"]] for row in label_rows)
        names = sorted(sizes)
        rng.shuffle(names)
        target = len(label_rows) * CHECK_SHARE
        taken = 0
        for name in names:
            # не берём группу, если с ней перескочим цель больше чем в 1.5 раза
            if taken < target and taken + sizes[name] <= target * 1.5:
                check_names.add(name)
                taken += sizes[name]
    tune = [row for row in rows if groups[row["id"]] not in check_names]
    check = [row for row in rows if groups[row["id"]] in check_names]
    return tune, check


def is_correct(row: dict, decision: RouteDecision) -> bool:
    label = row["label"]
    if label == "NONE":
        return decision.status is RouteStatus.NONE
    if label == "ASK":
        top_two = {c.app_id for c in decision.candidates[:2]}
        return decision.status is RouteStatus.AMBIGUOUS and top_two == set(
            row["candidates"]
        )
    return decision.status is RouteStatus.MATCHED and decision.app_id == label


def short_answer(decision: RouteDecision) -> str:
    # Короткая запись ответа роутера для таблицы ошибок
    if decision.status is RouteStatus.MATCHED:
        return str(decision.app_id)
    if decision.status is RouteStatus.AMBIGUOUS:
        a, b = decision.candidates[:2]
        return f"ASK[{a.app_id}/{b.app_id}]"
    return "NONE"


def report(title: str, rows: list[dict], router: ToolRouterService) -> list:
    errors = []
    right_by_label: Counter = Counter()
    total_by_label: Counter = Counter()
    for row in rows:
        decision = router(
            RouterInput(chat_id=uuid4(), project_id=None, text=row["text"])
        )
        total_by_label[row["label"]] += 1
        if is_correct(row, decision):
            right_by_label[row["label"]] += 1
        else:
            errors.append((row, decision))

    right = sum(right_by_label.values())
    print(f"\n== {title}: {right}/{len(rows)} = {right / len(rows):.1%}")
    for label in sorted(total_by_label):
        r, t = right_by_label[label], total_by_label[label]
        print(f"   {label:16} {r:3}/{t:<3} {r / t:.0%}")
    return errors


def print_short_stems(rows: list[dict]) -> None:
    # Для основ короче 5 букв: какие слова части tune они находят
    words = Counter(
        word for row in rows for word in re.findall(r"\w+", normalize_text(row["text"]))
    )
    print("\n== Короткие основы (< 5 букв) и найденные слова в tune")
    for name, stems in STEMS.items():
        for stem in stems:
            if len(stem) < 5:
                found = sorted(w for w in words if w.startswith(stem))
                print(f"   {name:16} {stem!r:10} -> {', '.join(found) or '(нет)'}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", type=Path, default=CORPUS_DIR / "dev.jsonl")
    parser.add_argument("--groups", type=Path, default=None)
    parser.add_argument("--errors", action="store_true")
    parser.add_argument("--short-stems", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    groups_path = args.groups or args.dev.parent / "groups.json"

    rows = read_jsonl(args.dev)
    groups = json.loads(groups_path.read_text(encoding="utf-8"))
    tune, check = split_by_groups(rows, groups)
    router = ToolRouterService(
        rules_scorer, THRESHOLD, MARGIN, load_app_versions(MANIFESTS_DIR)
    )

    tune_errors = report("tune (подбор)", tune, router)
    if args.check:
        report("check (проверка)", check, router)

    if args.errors:
        print("\n== Ошибки tune: ожидали -> получили | текст")
        for row, decision in tune_errors:
            expected = row["label"]
            if expected == "ASK":
                expected = "ASK[" + "/".join(row["candidates"]) + "]"
            print(f"   {expected:40} -> {short_answer(decision):40} | {row['text']}")
    if args.short_stems:
        print_short_stems(tune)


if __name__ == "__main__":
    main()
