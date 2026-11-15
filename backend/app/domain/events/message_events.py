from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from app.domain.events.events import DomainEvent

if TYPE_CHECKING:
    from app.domain.entities.message import MessageRole


@dataclass(frozen=True, kw_only=True)
class MessageEvent(DomainEvent):
    message_id: UUID
    chat_id: UUID
    role: "MessageRole"


class MessageCreated(MessageEvent): ...


class MessageContentUpdated(MessageEvent): ...


@dataclass(frozen=True, kw_only=True)
class MessageAttachmentCreated(DomainEvent):
    attachment_id: UUID
    chat_id: UUID


@dataclass(frozen=True, kw_only=True)
class MessageAttachmentConnectedMessage(MessageAttachmentCreated):
    message_id: UUID
