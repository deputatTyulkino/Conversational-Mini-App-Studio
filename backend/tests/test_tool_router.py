import json
from pathlib import Path
from uuid import uuid4

import pytest

from app.application.schemas.tool_router.tool_router_schema import (
    RouteDecision,
    RouteFallbackReason,
    RouterInput,
    RouteStatus,
)
from app.application.services.tool_router.rules import NONE_BONUS, rules_scorer
from app.application.services.tool_router.tool_router_service import (
    NONE_CLASS,
    ToolRouterService,
    build_decision,
    choose_status,
    load_app_versions,
    normalize_text,
    rank,
)

THRESHOLD = 0.55
MARGIN = 0.10
VERSIONS = {
    "research_board": "1.0.0",
    "project_planner": "1.0.0",
    "data_explorer": "1.0.0",
}


def scores(rb: float, pp: float, de: float, none: float) -> dict[str, float]:
    # Короткая запись оценок в порядке: research_board, project_planner, data_explorer, none
    return {
        "research_board": rb,
        "project_planner": pp,
        "data_explorer": de,
        NONE_CLASS: none,
    }


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        # регистр
        ("Посчитай ИТОГИ", "посчитай итоги"),
        # ё -> е, в том числе заглавная Ё
        ("Ещё отчёт", "еще отчет"),
        ("ЁЛКА", "елка"),
        # лишние пробелы, переносы строк и табуляция схлопываются в один пробел
        ("итоги   по\nмесяцам", "итоги по месяцам"),
        ("итоги\tпо\r\nмесяцам", "итоги по месяцам"),
        # неразрывный пробел (часто приходит при копировании из Word или браузера)
        ("итоги по месяцам", "итоги по месяцам"),
        # пробелы по краям убираются
        ("  успею к пятнице  ", "успею к пятнице"),
        # цифры, дефисы и знаки препинания остаются: это полезные признаки
        ("успею к 20-му?", "успею к 20-му?"),
        ("CSV, JSON и т.д.", "csv, json и т.д."),
        # пустая строка и строка из одних пробелов не ломают функцию
        ("", ""),
        ("   \n\t ", ""),
    ],
)
def test_normalize_text(raw: str, expected: str) -> None:
    assert normalize_text(raw) == expected


def test_normalize_text_is_idempotent() -> None:
    text = "  Ещё ОТЧЁТ\nпо   таблице? "
    once = normalize_text(text)
    assert normalize_text(once) == once


# ---------- rank ----------


def test_rank_sorts_by_score_descending() -> None:
    ranked = rank({"a": 0.1, "b": 0.7, "c": 0.2})
    assert ranked == [("b", 0.7), ("c", 0.2), ("a", 0.1)]


# ---------- choose_status ----------


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        # явный лидер-приложение
        (scores(0.05, 0.80, 0.10, 0.05), "matched"),
        # явный лидер none
        (scores(0.05, 0.10, 0.10, 0.75), "none"),
        # два приложения ниже порога и близко друг к другу
        (scores(0.04, 0.48, 0.42, 0.06), "ambiguous"),
        # выше порога, отрыв 0.25
        (scores(0.02, 0.60, 0.35, 0.03), "matched"),
        # выше порога, но отрыв всего 0.05
        (scores(0.02, 0.60, 0.55, 0.03), "ambiguous"),
        # не уверены, и второе место у none -> не спрашиваем, отвечаем текстом
        (scores(0.45, 0.10, 0.05, 0.40), "none"),
        # ambiguous бывает только между двумя приложениями
        (scores(0.02, 0.55, 0.03, 0.60), "none"),
        # граница: 0.60 - 0.50 без round дало бы 0.0999... < 0.10
        (scores(0.0, 0.60, 0.50, 0.0), "matched"),
    ],
)
def test_choose_status(given: dict[str, float], expected: str) -> None:
    assert choose_status(given, THRESHOLD, MARGIN) == expected


def test_choose_status_single_option() -> None:
    # один вариант: второе место считается 0.0, ambiguous невозможен
    assert choose_status({"project_planner": 0.9}, THRESHOLD, MARGIN) == "matched"
    assert choose_status({"project_planner": 0.3}, THRESHOLD, MARGIN) == "none"


# ---------- build_decision ----------


def assert_candidates_ok(decision: RouteDecision) -> None:
    ids = [c.app_id for c in decision.candidates]
    assert NONE_CLASS not in ids
    got = [c.score for c in decision.candidates]
    assert got == sorted(got, reverse=True)


def test_build_decision_matched() -> None:
    decision = build_decision(
        scores(0.05, 0.80, 0.10, 0.05), THRESHOLD, MARGIN, VERSIONS
    )
    assert decision.status is RouteStatus.MATCHED
    assert decision.app_id == "project_planner"
    assert decision.manifest_version == "1.0.0"
    assert decision.fallback_reason is None
    assert decision.confidence == 0.80
    assert decision.margin == 0.70
    assert_candidates_ok(decision)


def test_build_decision_ambiguous() -> None:
    decision = build_decision(
        scores(0.04, 0.48, 0.42, 0.06), THRESHOLD, MARGIN, VERSIONS
    )
    assert decision.status is RouteStatus.AMBIGUOUS
    assert decision.app_id is None
    assert decision.manifest_version is None
    first, second = decision.candidates[:2]
    assert (first.app_id, second.app_id) == ("project_planner", "data_explorer")
    assert_candidates_ok(decision)


def test_build_decision_none() -> None:
    decision = build_decision(
        scores(0.05, 0.10, 0.10, 0.75), THRESHOLD, MARGIN, VERSIONS
    )
    assert decision.status is RouteStatus.NONE
    assert decision.app_id is None
    assert decision.fallback_reason is RouteFallbackReason.NO_MATCH
    assert len(decision.candidates) == 3
    assert_candidates_ok(decision)


def test_build_decision_skips_disabled_app() -> None:
    # project_planner выключен (его нет в версиях) -> не выбирается и не в кандидатах
    versions = {"research_board": "1.0.0", "data_explorer": "1.0.0"}
    decision = build_decision(
        scores(0.02, 0.80, 0.10, 0.08), THRESHOLD, MARGIN, versions
    )
    assert decision.app_id != "project_planner"
    assert "project_planner" not in [c.app_id for c in decision.candidates]
    # оценки не перенормируются: остались de 0.10, none 0.08, rb 0.02
    # -> ниже порога, второе место у none -> none
    assert decision.status is RouteStatus.NONE
    assert_candidates_ok(decision)


def test_build_decision_empty_scores() -> None:
    with pytest.raises(ValueError):
        build_decision({}, THRESHOLD, MARGIN, VERSIONS)


# ---------- ToolRouterService ----------


def test_router_normalizes_text_before_scorer() -> None:
    seen: list[str] = []

    def fake_scorer(text: str) -> dict[str, float]:
        seen.append(text)  # запоминаем, какой текст пришёл в scorer
        return scores(0.05, 0.80, 0.10, 0.05)

    router = ToolRouterService(fake_scorer, THRESHOLD, MARGIN, VERSIONS)
    data = RouterInput(chat_id=uuid4(), project_id=None, text="Ещё  ЗАДАЧА\nк пятнице")
    decision = router(data)

    assert seen == ["еще задача к пятнице"]
    assert decision.status is RouteStatus.MATCHED
    assert decision.app_id == "project_planner"


def test_router_with_lambda_scorer() -> None:
    router = ToolRouterService(
        lambda text: scores(0.0, 0.0, 0.0, 1.0), THRESHOLD, MARGIN, VERSIONS
    )
    decision = router(RouterInput(chat_id=uuid4(), project_id=None, text="привет"))
    assert decision.status is RouteStatus.NONE


# ---------- load_app_versions ----------


def write_manifest(folder: Path, app_id: str, enabled: bool) -> None:
    data = {"id": app_id, "version": "2.1.0", "enabled": enabled, "name": "Тест"}
    (folder / f"{app_id}.json").write_text(json.dumps(data), encoding="utf-8")


def test_load_app_versions_only_enabled(tmp_path: Path) -> None:
    write_manifest(tmp_path, "research_board", enabled=True)
    write_manifest(tmp_path, "data_explorer", enabled=False)
    assert load_app_versions(tmp_path) == {"research_board": "2.1.0"}


def test_load_app_versions_empty_folder(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="манифест"):
        load_app_versions(tmp_path)


def test_load_app_versions_missing_folder(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError):
        load_app_versions(tmp_path / "nope")


def test_real_manifests_load() -> None:
    # настоящие манифесты проекта читаются (без .env и настроек)
    from app.application.services.tool_router.tool_router_service import MANIFESTS_DIR

    # сравниваем только названия: версии манифестов могут меняться
    assert set(load_app_versions(MANIFESTS_DIR)) == set(VERSIONS)


# ---------- rules_scorer ----------


def test_rules_scorer_returns_four_classes_summing_to_one() -> None:
    result = rules_scorer("успею ли я сдать курсовую")
    assert set(result) == set(VERSIONS) | {NONE_CLASS}
    assert abs(sum(result.values()) - 1.0) < 1e-9


def test_rules_scorer_empty_text_is_none() -> None:
    # слов нет -> очки только у none (фора) -> none = 1.0
    assert NONE_BONUS > 0
    assert rules_scorer("")[NONE_CLASS] == 1.0


def test_rules_scorer_stem_matches_word_forms() -> None:
    # основа «задач» находит разные формы слова
    for text in ["одна задача", "две задачи", "сделай задачу"]:
        result = rules_scorer(text)
        assert result["project_planner"] > result[NONE_CLASS]


def test_rules_scorer_ignores_punctuation() -> None:
    assert rules_scorer("таблица, csv!") == rules_scorer("таблица csv")


def test_rules_scorer_stem_counts_once() -> None:
    # повтор одного слова не добавляет очков
    assert rules_scorer("задача задача задача") == rules_scorer("задача")


def test_rules_scorer_phrase_from_word_start() -> None:
    # фраза «что такое» найдена, а внутри другого слова — нет
    assert (
        rules_scorer("что такое дедлайн")[NONE_CLASS]
        > rules_scorer("дедлайн")[NONE_CLASS]
    )
    assert rules_scorer("нечто такое") == rules_scorer("")


def test_router_with_rules_examples() -> None:
    router = ToolRouterService(rules_scorer, THRESHOLD, MARGIN, VERSIONS)

    def ask(text: str) -> RouteDecision:
        return router(RouterInput(chat_id=uuid4(), project_id=None, text=text))

    # таблица (data_explorer) + задачи (project_planner), цели нет -> спросить
    decision = ask("Вот таблица с задачами, разберись с ней")
    assert decision.status is RouteStatus.AMBIGUOUS
    top_two = {c.app_id for c in decision.candidates[:2]}
    assert top_two == {"project_planner", "data_explorer"}

    # обычный разговор -> ответить текстом
    assert ask("привет, как дела?").status is RouteStatus.NONE


def test_rules_scorer_ignores_quoted_titles() -> None:
    # R9: слова из названия в «кавычках» не дают очков
    titled = rules_scorer("вычитку книги «большие данные и таблицы» сдвинь")
    plain = rules_scorer("вычитку книги сдвинь")
    assert titled == plain
