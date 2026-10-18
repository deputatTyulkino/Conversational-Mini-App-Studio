from collections.abc import Sequence
from typing import ClassVar, Self
from uuid import UUID

from app.application.schemas.chat import ChatRead
from app.application.schemas.common import (
    InputSchema,
    PatchSchema,
    ProjectDescription,
    ProjectName,
    ReadSchema,
)
from app.domain.entities.chat import Chat
from app.domain.entities.project import Project
from pydantic import AwareDatetime, Field, computed_field


class ProjectRead(ReadSchema):
    id: UUID
    name: str
    description: str | None
    created_at: AwareDatetime
    updated_at: AwareDatetime


class ProjectWithChatsRead(ProjectRead):
    chats: list[ChatRead] = Field(default_factory=list)

    @computed_field
    @property
    def last_activity_at(self) -> AwareDatetime:
        return max([self.updated_at, *(chat.updated_at for chat in self.chats)])

    @classmethod
    def build(cls, project: Project, chats: Sequence[Chat]) -> Self:
        return cls(
            **ProjectRead.model_validate(project).model_dump(),
            chats=[ChatRead.model_validate(chat) for chat in chats],
        )


class ProjectCreate(InputSchema):
    name: ProjectName
    description: ProjectDescription | None = None


class ProjectUpdate(PatchSchema):
    non_nullable_fields: ClassVar[frozenset[str]] = frozenset({"name"})

    name: ProjectName | None = None
    description: ProjectDescription | None = None
