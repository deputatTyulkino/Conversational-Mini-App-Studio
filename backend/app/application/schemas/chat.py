from typing import ClassVar
from uuid import UUID

from app.application.schemas.common import (
    ChatTitle,
    InputSchema,
    PatchSchema,
    ReadSchema,
)
from pydantic import AwareDatetime


class ChatRead(ReadSchema):
    id: UUID
    title: str
    project_id: UUID | None
    is_pinned: bool
    created_at: AwareDatetime
    updated_at: AwareDatetime


class ChatCreate(InputSchema):
    title: ChatTitle | None = None
    project_id: UUID | None = None


class ChatUpdate(PatchSchema):
    non_nullable_fields: ClassVar[frozenset[str]] = frozenset({"title", "is_pinned"})

    title: ChatTitle | None = None
    is_pinned: bool | None = None
    project_id: UUID | None = None
