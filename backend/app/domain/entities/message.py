from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from app.domain.common import utcnow
from app.domain.exceptions import DomainValidationError

MAX_MESSAGE_LENGTH = 20_000


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass(frozen=True, slots=True)
class Message:
    id: UUID
    chat_id: UUID
    role: MessageRole
    content: str
    payload: dict[str, Any] | None = None
    created_at: datetime = field(default_factory=utcnow)

    def __post_init__(self) -> None:
        if len(self.content) > MAX_MESSAGE_LENGTH:
            raise DomainValidationError(
                f"Сообщение длиннее {MAX_MESSAGE_LENGTH} символов"
            )
        if not self.content.strip() and (
            self.payload is None or self.role is MessageRole.USER
        ):
            raise DomainValidationError("Пустое сообщение недопустимо")

    @classmethod
    def create(
        cls,
        *,
        chat_id: UUID,
        role: MessageRole,
        content: str,
        payload: dict[str, Any] | None = None,
    ) -> "Message":
        return cls(
            id=uuid4(), chat_id=chat_id, role=role, content=content, payload=payload
        )
