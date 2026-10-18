from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.message import MessageRole
from app.domain.events.events import DomainEvent


@dataclass(frozen=True, kw_only=True)
class ChatEvent(DomainEvent):
    chat_id: UUID
    project_id: UUID | None


class ChatCreated(ChatEvent): ...


class ChatRenamed(ChatEvent): ...


class ChatPinned(ChatEvent): ...


class ChatUnpinned(ChatEvent): ...


class ChatDeleted(ChatEvent): ...


@dataclass(frozen=True, kw_only=True)
class ChatMovedToProject(ChatEvent):
    previous_project_id: UUID | None


@dataclass(frozen=True, kw_only=True)
class MessageAdded(ChatEvent):
    message_id: UUID
    role: MessageRole
