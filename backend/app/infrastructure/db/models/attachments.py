import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from app.infrastructure.db.config import Base
from app.infrastructure.storage.local_file_storage import MAX_ORIGINAL_NAME_LENGTH
from sqlalchemy import (
    UUID,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.infrastructure.db.models.chats import ChatORM
    from app.infrastructure.db.models.messages import MessageORM


class AttachmentORM(Base):
    __tablename__ = "attachments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    chat_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"), nullable=True
    )
    message_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("messages.id", ondelete="CASCADE"), nullable=True
    )
    stored_name: Mapped[str]
    relative_path: Mapped[str]
    original_name: Mapped[str] = mapped_column(String(MAX_ORIGINAL_NAME_LENGTH))
    content_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    extension: Mapped[str] = mapped_column(String(10))
    size: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    message: Mapped["MessageORM | None"] = relationship(
        back_populates="attachments", lazy="raise"
    )
    chat: Mapped["ChatORM | None"] = relationship(
        back_populates="attachments", lazy="raise"
    )

    __table_args__ = (
        CheckConstraint("size > 0", name="size_positive"),
        Index("ix_message_attachments", chat_id, message_id),
        Index(
            "ix_attachments_created_at_null",
            text("created_at"),
            postgresql_where=text("message_id IS NULL"),
        ),
    )
