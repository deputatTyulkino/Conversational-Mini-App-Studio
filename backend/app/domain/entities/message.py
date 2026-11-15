from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from app.domain.common import AggregateRoot, utcnow
from app.domain.entities.attachment import AttachmentDomain
from app.domain.events.message_events import MessageContentUpdated, MessageCreated
from app.domain.exceptions.message import (
    MessageContentEmptyError,
    MessageContentTooLongError,
    MessageNotEditableError,
)

MAX_MESSAGE_LENGTH = 20_000
ERROR_MESSAGE = "Пустое сообщение недопустимо"


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass(eq=False)
class MessageDomain(AggregateRoot):
    id: UUID
    chat_id: UUID
    role: MessageRole
    content: str
    payload: dict[str, Any] | None = None
    created_at: datetime = field(default_factory=utcnow)
    attachments: list[AttachmentDomain] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.content) > MAX_MESSAGE_LENGTH:
            raise MessageContentTooLongError(MAX_MESSAGE_LENGTH)
        if not self.content.strip() and (
            self.payload is None or self.role is MessageRole.USER
        ):
            raise MessageContentEmptyError(ERROR_MESSAGE)

    @classmethod
    def create(
        cls,
        *,
        chat_id: UUID,
        role: MessageRole,
        content: str,
        payload: dict[str, Any] | None = None,
    ) -> "MessageDomain":
        message = cls(
            id=uuid4(),
            chat_id=chat_id,
            role=role,
            content=content,
            payload=payload,
        )
        message._record(
            MessageCreated(
                message_id=message.id, chat_id=message.chat_id, role=message.role
            )
        )
        return message

    def change_content(self, content: str) -> None:
        if self.role is not MessageRole.USER:
            raise MessageNotEditableError()
        content = content.strip()
        if not content:
            raise MessageContentEmptyError(ERROR_MESSAGE)
        if len(content) > MAX_MESSAGE_LENGTH:
            raise MessageContentTooLongError(MAX_MESSAGE_LENGTH)
        if content == self.content:
            return
        self.content = content
        self._record(
            MessageContentUpdated(
                message_id=self.id, chat_id=self.chat_id, role=self.role
            )
        )

    def replace_attachments(self, attachments: list[AttachmentDomain]) -> None:
        self.attachments = list(attachments)
