from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.common import AggregateRoot, utcnow
from app.domain.events.message_events import (
    MessageAttachmentConnectedMessage,
    MessageAttachmentCreated,
)
from app.domain.exceptions.attachment import AttachmentNotAvailableError
from app.domain.value_objects.file import StoredFile


@dataclass(eq=False)
class AttachmentDomain(AggregateRoot):
    id: UUID
    chat_id: UUID
    relative_path: str
    original_name: str
    extension: str
    size: int
    message_id: UUID | None = None
    content_type: str | None = None
    created_at: datetime = field(default_factory=utcnow)

    def to_value_object(self) -> StoredFile:
        return StoredFile(
            relative_path=self.relative_path,
            original_name=self.original_name,
            extension=self.extension,
            content_type=self.content_type,
            size=self.size,
        )

    @classmethod
    def create(
        cls,
        chat_id: UUID,
        relative_path: str,
        original_name: str,
        extension: str,
        size: int,
        content_type: str | None = None,
        message_id: UUID | None = None,
    ):
        attachment = cls(
            id=uuid4(),
            chat_id=chat_id,
            message_id=message_id,
            relative_path=relative_path,
            original_name=original_name,
            extension=extension,
            content_type=content_type,
            size=size,
        )
        attachment._record(
            MessageAttachmentCreated(
                attachment_id=attachment.id,
                chat_id=attachment.chat_id,
            )
        )
        return attachment

    def attach_to_message(self, message_id: UUID) -> None:
        if self.message_id not in (None, message_id):
            raise AttachmentNotAvailableError([self.id])
        self.message_id = message_id
        self._record(
            MessageAttachmentConnectedMessage(
                attachment_id=self.id, chat_id=self.chat_id, message_id=message_id
            )
        )
