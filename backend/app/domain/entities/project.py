# domain/entities/project.py
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.common import AggregateRoot, require_text, utcnow
from app.domain.entities.chat import DEFAULT_CHAT_TITLE, Chat
from app.domain.events.project_events import (
    ProjectCreated,
    ProjectDeleted,
    ProjectUpdated,
)

MAX_PROJECT_NAME_LENGTH = 255
MAX_PROJECT_DESCRIPTION_LENGTH = 2000


@dataclass(eq=False)
class Project(AggregateRoot):
    id: UUID
    name: str
    description: str | None = None
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)

    @classmethod
    def create(cls, name: str, description: str | None = None) -> "Project":
        project = cls(
            id=uuid4(),
            name=require_text(name, "Название проекта", MAX_PROJECT_NAME_LENGTH),
            description=description,
        )
        project._record(ProjectCreated(project_id=project.id))
        return project

    def rename(self, name: str) -> None:
        name = require_text(name, "Название проекта", MAX_PROJECT_NAME_LENGTH)
        if name == self.name:
            return
        self.name = name
        self._touch("name")

    def change_description(self, description: str | None) -> None:
        description = (description or "").strip() or None
        if description == self.description:
            return
        self.description = description
        self._touch("description")

    def create_chat(self, title: str = DEFAULT_CHAT_TITLE) -> Chat:
        return Chat.create(title=title, project_id=self.id)

    def mark_deleted(self) -> None:
        self._record(ProjectDeleted(project_id=self.id))

    def _touch(self, *changed: str) -> None:
        self.updated_at = utcnow()
        self._record(ProjectUpdated(project_id=self.id, fields=changed))
