from enum import StrEnum
from typing import Annotated, Any, Literal, Self
from uuid import UUID

from app.application.schemas.common import ReadSchema
from app.domain.value_objects.file import StoredFile
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

AppId = Annotated[str, StringConstraints(pattern=r"^[a-z][a-z0-9_]{1,63}$")]
Score = Annotated[float, Field(ge=0.0, le=1.0)]


class RouterInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    chat_id: UUID = Field(description="Чат, в который пришло сообщение")
    project_id: UUID | None = Field(description="Проект чата, None для отдельного чата")
    text: str = Field(
        description="Текст сообщения пользователя, уже очищенный от пробелов"
    )
    attachments: list[StoredFile] = Field(
        default_factory=list,
        description="Файлы сообщения, уже сохранённые в хранилище",
    )


class RouteStatus(StrEnum):
    MATCHED = "matched"
    AMBIGUOUS = "ambiguous"
    NONE = "none"


class RouteFallbackReason(StrEnum):
    NO_MATCH = "no_match"
    ROUTER_ERROR = "router_error"


class RouteCandidate(ReadSchema):
    app_id: AppId
    score: Score
    reasons: list[str] = Field(default_factory=list)


class RouteDecision(ReadSchema):
    status: RouteStatus
    app_id: AppId | None = None
    manifest_version: str | None = None
    confidence: Score
    margin: Score = 0.0
    candidates: list[RouteCandidate] = Field(default_factory=list)
    params: dict[str, Any] = Field(default_factory=dict)
    fallback_reason: RouteFallbackReason | None = None

    @model_validator(mode="after")
    def _check_consistency(self) -> Self:
        if self.status is RouteStatus.MATCHED:
            if self.app_id is None or self.manifest_version is None:
                raise ValueError("Для matched нужны app_id и manifest_version")
            if self.fallback_reason is not None:
                raise ValueError("Для matched fallback_reason должен быть пустым")
        else:
            if self.app_id is not None or self.manifest_version is not None:
                raise ValueError(
                    "app_id и manifest_version задаются только для matched"
                )
            if self.params:
                raise ValueError("params задаются только для matched")
        if self.status is RouteStatus.NONE and self.fallback_reason is None:
            raise ValueError("Для none нужен fallback_reason")
        if self.status is RouteStatus.AMBIGUOUS and len(self.candidates) < 2:
            raise ValueError("Для ambiguous нужно минимум два кандидата")
        scores = [candidate.score for candidate in self.candidates]
        if scores != sorted(scores, reverse=True):
            raise ValueError("Кандидаты должны идти по убыванию score")
        return self


class RoutePayload(ReadSchema):
    type: Literal["route"] = "route"
    decision: RouteDecision
