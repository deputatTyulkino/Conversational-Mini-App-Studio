from collections.abc import Sequence
from typing import Any, Self
from uuid import UUID

from app.application.schemas.common import InputSchema, MessageContent, ReadSchema
from app.domain.entities.message import Message, MessageRole
from pydantic import AwareDatetime, Field, field_validator


class MessageRead(ReadSchema):
    id: UUID
    chat_id: UUID
    role: MessageRole
    content: str
    payload: dict[str, Any] | None = None
    created_at: AwareDatetime


class MessageCreate(InputSchema):
    content: MessageContent
    client_message_id: UUID | None = None

    @field_validator("content")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Сообщение не может состоять из пробелов")
        return value


class SendMessageResponse(ReadSchema):
    user_message: MessageRead
    assistant_message: MessageRead | None = None


class MessageListParams(InputSchema):
    limit: int = Field(default=100, ge=1, le=200)
    before: UUID | None = None


class MessagePage(ReadSchema):
    items: list[MessageRead]
    has_more: bool
    next_cursor: UUID | None = None

    @classmethod
    def build(cls, messages: Sequence[Message], limit: int) -> Self:
        has_more = len(messages) > limit
        page = messages[1:] if has_more else messages
        items = [MessageRead.model_validate(m) for m in page]
        return cls(
            items=items,
            has_more=has_more,
            next_cursor=items[0].id if has_more else None,
        )
