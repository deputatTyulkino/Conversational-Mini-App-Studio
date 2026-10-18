import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from app.domain.entities.message import MessageRole
from app.infrastructure.db.config import Base
from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Index, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.infrastructure.db.models.chats import ChatORM


class MessageORM(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    chat_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[MessageRole] = mapped_column(
        Enum(
            MessageRole,
            native_enum=False,
            length=16,
            values_callable=lambda e: [m.value for m in e],
        ),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    chat: Mapped["ChatORM"] = relationship(back_populates="messages", lazy="raise")

    __table_args__ = (
        CheckConstraint(
            "content <> '' OR payload IS NOT NULL", name="content_or_payload"
        ),
        Index("ix_messages_chat_id_created_at_id", "chat_id", "created_at", "id"),
    )
