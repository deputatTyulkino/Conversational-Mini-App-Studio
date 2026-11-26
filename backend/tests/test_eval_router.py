import pytest
from app.application.schemas.tool_router.tool_router_schema import (
    RouteDecision,
    RouterInput,
)
from app.application.services.tool_router.tool_router_service import ToolRouterService
from scripts.eval_router import report


def test_report_confusion_matrix_and_metrics(
    capsys: pytest.CaptureFixture[str],
) -> None:
    research = "research_board"
    planner = "project_planner"
    explorer = "data_explorer"
    rows = [
        {"text": "0", "label": research},
        {"text": "1", "label": research},
        {"text": "2", "label": research},
        {"text": "3", "label": planner},
        {"text": "4", "label": planner},
        {"text": "5", "label": explorer},
        {"text": "6", "label": "NONE"},
        {"text": "7", "label": "ASK", "candidates": [planner, research]},
        {"text": "8", "label": "ASK", "candidates": [planner, explorer]},
    ]
    scores = [
        {research: 1.0},
        {planner: 1.0},
        {planner: 1.0},
        {research: 1.0},
        {planner: 1.0},
        {planner: 1.0},
        {"none": 1.0},
        {research: 0.5, planner: 0.5},
        {research: 0.5, planner: 0.5},
    ]
    router = ToolRouterService(
        lambda text: scores[int(text)],
        threshold=0.55,
        margin=0.10,
        app_versions=dict.fromkeys((research, planner, explorer), "1.0.0"),
    )
    calls = []

    def route(data: RouterInput) -> RouteDecision:
        calls.append(data.text)
        return router(data)

    errors = report("пример", rows, route)
    lines = [
        " ".join(line.split())
        for line in capsys.readouterr().out.splitlines()
        if line.strip()
    ]

    assert calls == [row["text"] for row in rows]
    assert [row["text"] for row, _ in errors] == ["1", "2", "3", "5", "8"]
    assert lines == [
        "== пример: 4/9 = 44.4%",
        "Матрица ошибок (строки — эталон, столбцы — предсказание)",
        "Метка research_board project_planner data_explorer NONE ASK",
        "research_board 1 2 0 0 0",
        "project_planner 1 1 0 0 0",
        "data_explorer 0 1 0 0 0",
        "NONE 0 0 0 1 0",
        "ASK 0 0 0 0 2",
        "Сумма ячеек: 9",
        "Метка Precision Recall",
        "research_board 1/2 = 50.0% 1/3 = 33.3%",
        "project_planner 1/4 = 25.0% 1/2 = 50.0%",
        "data_explorer — 0/1 = 0.0%",
        "NONE 1/1 = 100.0% 1/1 = 100.0%",
        "ASK 2/2 = 100.0% 2/2 = 100.0%",
        "Совпала пара в ASK → ASK: 1/2",
    ]
