from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from app.domain.common import AggregateRoot, utcnow
from app.domain.entities.message import MessageDomain, MessageRole
from app.domain.events.chat_events import (
    ChatCreated,
    ChatDeleted,
    ChatMovedToProject,
    ChatPinned,
    ChatRenamed,
    ChatUnpinned,
    MessageAdded,
)
from app.domain.exceptions.chat import ChatTitleEmptyError, ChatTitleTooLongError

DEFAULT_CHAT_TITLE = "Новый чат"
MAX_CHAT_TITLE_LENGTH = 255
CHAT_FIELD_NAME = "Название чата"


@dataclass(eq=False)
class ChatDomain(AggregateRoot):
    id: UUID
    title: str
    project_id: UUID | None = None
    is_pinned: bool = False
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)

    @staticmethod
    def _normalize_title(title: str) -> str:
        title = title.strip()
        if not title:
            raise ChatTitleEmptyError(f"{CHAT_FIELD_NAME} не может быть пустым")
        if len(title) > MAX_CHAT_TITLE_LENGTH:
            raise ChatTitleTooLongError(MAX_CHAT_TITLE_LENGTH)
        return title

    @classmethod
    def create(
        cls, title: str = DEFAULT_CHAT_TITLE, project_id: UUID | None = None
    ) -> "ChatDomain":
        chat = cls(
            id=uuid4(),
            title=cls._normalize_title(title),
            project_id=project_id,
        )
        chat._record(ChatCreated(chat_id=chat.id, project_id=chat.project_id))
        return chat

    def rename(self, title: str) -> None:
        title = self._normalize_title(title)
        if title == self.title:
            return
        self.title = title
        self._touch()
        self._record(ChatRenamed(chat_id=self.id, project_id=self.project_id))

    def pin(self) -> None:
        if self.is_pinned:
            return
        self.is_pinned = True
        self._record(ChatPinned(chat_id=self.id, project_id=self.project_id))

    def unpin(self) -> None:
        if not self.is_pinned:
            return
        self.is_pinned = False
        self._record(ChatUnpinned(chat_id=self.id, project_id=self.project_id))

    def move_to_project(self, project_id: UUID | None) -> None:
        if project_id == self.project_id:
            return
        previous, self.project_id = self.project_id, project_id
        self._touch()
        self._record(
            ChatMovedToProject(
                chat_id=self.id, project_id=project_id, previous_project_id=previous
            )
        )

    def add_message(
        self,
        role: MessageRole,
        content: str,
        payload: dict[str, Any] | None = None,
    ) -> MessageDomain:
        message = MessageDomain.create(
            chat_id=self.id, role=role, content=content, payload=payload
        )
        self.updated_at = message.created_at
        self._record(
            MessageAdded(
                chat_id=self.id,
                project_id=self.project_id,
                message_id=message.id,
                role=message.role,
            )
        )
        return message

    def mark_deleted(self) -> None:
        self._record(ChatDeleted(chat_id=self.id, project_id=self.project_id))

    def _touch(self) -> None:
        self.updated_at = utcnow()
