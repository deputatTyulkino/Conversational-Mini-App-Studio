import json
from collections.abc import Callable
from pathlib import Path

from app.application.schemas.tool_router.tool_router_schema import (
    RouteCandidate,
    RouteDecision,
    RouteFallbackReason,
    RouterInput,
    RouteStatus,
)
from app.config.settings import get_settings

NONE_CLASS = "none"

# Функция оценки: получает текст, возвращает оценки четырёх классов
Scorer = Callable[[str], dict[str, float]]

# Папка backend/manifests. Считаем от этого файла, а не от текущей папки:
# parents[0]=tool_router, [1]=services, [2]=application, [3]=app, [4]=backend
MANIFESTS_DIR = Path(__file__).resolve().parents[4] / "manifests"


def normalize_text(text: str) -> str:
    text = text.lower().replace("ё", "е")
    return " ".join(text.split())


def rank(scores: dict[str, float]) -> list[tuple[str, float]]:
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)


def choose_status(scores: dict[str, float], threshold: float, margin: float) -> str:
    ranked = rank(scores)
    best_name, best_score = ranked[0]
    second_name, second_score = ranked[1] if len(ranked) > 1 else (None, 0.0)
    gap = round(best_score - second_score, 6)

    confident = best_score >= threshold and gap >= margin
    if confident:
        return "none" if best_name == NONE_CLASS else "matched"

    apps = (NONE_CLASS, None)
    if best_name not in apps and second_name not in apps:
        return "ambiguous"
    return "none"


def build_decision(
    scores: dict[str, float],
    threshold: float,
    margin: float,
    app_versions: dict[str, str],
) -> RouteDecision:
    scores = {
        name: score
        for name, score in scores.items()
        if name in app_versions or name == NONE_CLASS
    }
    if not scores:
        raise ValueError("Нет оценок ни для одного включённого класса")

    status = choose_status(scores, threshold, margin)

    ranked = rank(scores)
    best_name, best_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else 0.0
    gap = round(best_score - second_score, 6)

    candidates = [
        RouteCandidate(app_id=name, score=score)
        for name, score in ranked
        if name != NONE_CLASS
    ]

    if status == "matched":
        return RouteDecision(
            status=RouteStatus.MATCHED,
            app_id=best_name,
            manifest_version=app_versions[best_name],
            confidence=best_score,
            margin=gap,
            candidates=candidates,
        )
    if status == "ambiguous" and len(candidates) >= 2:
        return RouteDecision(
            status=RouteStatus.AMBIGUOUS,
            confidence=best_score,
            margin=gap,
            candidates=candidates,
        )
    return RouteDecision(
        status=RouteStatus.NONE,
        confidence=best_score,
        margin=gap,
        candidates=candidates,
        fallback_reason=RouteFallbackReason.NO_MATCH,
    )


class ToolRouterService:
    def __init__(
        self,
        scorer: Scorer,
        threshold: float,
        margin: float,
        app_versions: dict[str, str],
    ) -> None:
        self.scorer = scorer
        self.threshold = threshold
        self.margin = margin
        self.app_versions = app_versions

    def __call__(self, data: RouterInput) -> RouteDecision:
        text = normalize_text(data.text)
        scores = self.scorer(text)
        return build_decision(scores, self.threshold, self.margin, self.app_versions)


def stub_scorer(text: str) -> dict[str, float]:
    # Временная заглушка пока нет правил по ключевым словам и модели
    return {
        "research_board": 0.0,
        "project_planner": 0.0,
        "data_explorer": 0.0,
        NONE_CLASS: 1.0,
    }


def load_app_versions(manifests_dir: Path) -> dict[str, str]:
    # Читаю манифесты и беру id и version у включённых приложений
    if not manifests_dir.is_dir():
        raise RuntimeError(f"Папка с манифестами не найдена: {manifests_dir}")
    paths = sorted(manifests_dir.glob("*.json"))
    if not paths:
        raise RuntimeError(f"В папке нет манифестов: {manifests_dir}")

    versions: dict[str, str] = {}
    for path in paths:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if manifest.get("enabled") is True:
            versions[manifest["id"]] = manifest["version"]
    return versions


def build_tool_router() -> ToolRouterService:
    settings = get_settings()
    return ToolRouterService(
        scorer=stub_scorer,
        threshold=settings.router_confidence_threshold,
        margin=settings.router_ambiguity_margin,
        app_versions=load_app_versions(MANIFESTS_DIR),
    )
