from dataclasses import dataclass
from uuid import UUID

from app.domain.events.events import DomainEvent


@dataclass(frozen=True, kw_only=True)
class ProjectEvent(DomainEvent):
    project_id: UUID


class ProjectCreated(ProjectEvent): ...


class ProjectDeleted(ProjectEvent): ...


@dataclass(frozen=True, kw_only=True)
class ProjectUpdated(ProjectEvent):
    fields: tuple[str, ...]
