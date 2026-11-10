from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.common import AggregateRoot, utcnow
from app.domain.entities.chat import DEFAULT_CHAT_TITLE, ChatDomain
from app.domain.events.project_events import (
    ProjectCreated,
    ProjectDeleted,
    ProjectUpdated,
)
from app.domain.exceptions.project import (
    ProjectDescriptionTooLongError,
    ProjectNameEmptyError,
    ProjectNameTooLongError,
)

MAX_PROJECT_NAME_LENGTH = 255
MAX_PROJECT_DESCRIPTION_LENGTH = 2000
FIELD_NAME = "Название проекта"


@dataclass(eq=False)
class ProjectDomain(AggregateRoot):
    id: UUID
    name: str
    description: str | None = None
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    chats: list[ChatDomain] = field(default_factory=list)

    @staticmethod
    def _normalize_name(name: str) -> str:
        name = name.strip()
        if not name:
            raise ProjectNameEmptyError(f"{FIELD_NAME} не может быть пустым")
        if len(name) > MAX_PROJECT_NAME_LENGTH:
            raise ProjectNameTooLongError(MAX_PROJECT_NAME_LENGTH)
        return name

    @staticmethod
    def _normalize_description(description: str | None) -> str | None:
        description = (description or "").strip() or None
        if (
            description is not None
            and len(description) > MAX_PROJECT_DESCRIPTION_LENGTH
        ):
            raise ProjectDescriptionTooLongError(MAX_PROJECT_DESCRIPTION_LENGTH)
        return description

    @classmethod
    def create(cls, name: str, description: str | None = None) -> "ProjectDomain":
        project = cls(
            id=uuid4(),
            name=cls._normalize_name(name),
            description=cls._normalize_description(description),
        )
        project._record(ProjectCreated(project_id=project.id))
        return project

    def rename(self, name: str) -> None:
        name = self._normalize_name(name)
        if name == self.name:
            return
        self.name = name
        self._touch("name")

    def change_description(self, description: str | None) -> None:
        description = self._normalize_description(description)
        if description == self.description:
            return
        self.description = description
        self._touch("description")

    def create_chat(self, title: str = DEFAULT_CHAT_TITLE) -> ChatDomain:
        chat = ChatDomain.create(title=title, project_id=self.id)
        self.chats.append(chat)
        self.updated_at = chat.created_at
        return chat

    def mark_deleted(self) -> None:
        self._record(ProjectDeleted(project_id=self.id))

    def _touch(self, *changed: str) -> None:
        self.updated_at = utcnow()
        self._record(ProjectUpdated(project_id=self.id, fields=changed))
