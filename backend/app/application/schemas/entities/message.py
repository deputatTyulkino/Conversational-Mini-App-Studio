from datetime import datetime
from typing import Annotated, Self
from uuid import UUID

from app.application.schemas.common import InputSchema, ReadSchema
from app.application.schemas.entities.attachment import AttachmentRead
from app.application.schemas.tool_router.tool_router_schema import RoutePayload
from app.domain.entities.message import MessageDomain, MessageRole
from pydantic import (
    AwareDatetime,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

MessageContent = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=4000),
]

MAX_ATTACHMENTS_PER_MESSAGE = 10


class MessageRead(ReadSchema):
    id: UUID
    chat_id: UUID
    role: MessageRole
    content: str
    payload: RoutePayload | None = None
    created_at: AwareDatetime
    attachments: list[AttachmentRead] = Field(default_factory=list)


class MessageBase(InputSchema):
    content: MessageContent
    attachment_ids: list[UUID] = Field(
        default_factory=list, max_length=MAX_ATTACHMENTS_PER_MESSAGE
    )

    @field_validator("attachment_ids")
    @classmethod
    def _unique_ids(cls, value: list[UUID]) -> list[UUID]:
        if len(set(value)) != len(value):
            raise ValueError("attachment_ids must be unique")
        return value


class MessageCreate(MessageBase):
    client_message_id: UUID


class MessageUpdate(MessageBase): ...


class SendMessageResponse(ReadSchema):
    client_message_id: UUID | None = None
    user_message: MessageRead
    assistant_message: MessageRead

    @classmethod
    def build(
        cls,
        client_message_id: UUID | None,
        user_message: MessageDomain,
        assistant_message: MessageDomain,
    ) -> "SendMessageResponse":
        return cls(
            client_message_id=client_message_id,
            user_message=MessageRead.model_validate(user_message),
            assistant_message=MessageRead.model_validate(assistant_message),
        )


class MessageListParams(InputSchema):
    limit: int = Field(default=100, ge=1, le=200)
    before_created_at: datetime | None = None
    before_id: UUID | None = None

    @model_validator(mode="after")
    def check_cursor_pair(self):
        if (self.before_created_at is None) != (self.before_id is None):
            raise ValueError("before_created_at и before_id нужно передавать вместе")
        return self


class MessagePage(ReadSchema):
    items: list[MessageRead]
    has_more: bool
    next_before_created_at: datetime | None = None
    next_before_id: UUID | None = None

    @classmethod
    def build(cls, messages: list[MessageDomain], limit: int) -> Self:
        has_more = len(messages) > limit
        page = messages[1:] if has_more else messages
        items = [MessageRead.model_validate(m) for m in page]
        oldest = items[0] if has_more else None
        return cls(
            items=items,
            has_more=has_more,
            next_before_created_at=oldest.created_at if oldest else None,
            next_before_id=oldest.id if oldest else None,
        )
