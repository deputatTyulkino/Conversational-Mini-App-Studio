from typing import Annotated, Self
from uuid import UUID

from app.application.schemas.common import InputSchema, ReadSchema
from app.application.schemas.tool_router.tool_router_schema import RoutePayload
from app.domain.entities.message import MessageDomain, MessageRole
from pydantic import AwareDatetime, Field, StringConstraints

MessageContent = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=4000),
]


class MessageRead(ReadSchema):
    id: UUID
    chat_id: UUID
    role: MessageRole
    content: str
    payload: RoutePayload | None = None
    created_at: AwareDatetime


class MessageCreate(InputSchema):
    content: MessageContent
    client_message_id: UUID


class MessageUpdate(MessageCreate): ...


class SendMessageResponse(ReadSchema):
    client_message_id: UUID
    user_message: MessageRead
    assistant_message: MessageRead


class MessageListParams(InputSchema):
    limit: int = Field(default=101, ge=1, le=200)
    before_id: UUID | None = None


class MessagePage(ReadSchema):
    items: list[MessageRead]
    has_more: bool
    next_cursor: UUID | None = None

    @classmethod
    def build(cls, messages: list[MessageDomain], limit: int) -> Self:
        has_more = len(messages) > limit
        page = messages[1:] if has_more else messages
        items = [MessageRead.model_validate(m) for m in page]
        return cls(
            items=items,
            has_more=has_more,
            next_cursor=items[0].id if has_more else None,
        )
