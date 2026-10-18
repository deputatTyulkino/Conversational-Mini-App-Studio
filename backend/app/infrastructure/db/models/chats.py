import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from app.infrastructure.db.config import Base
from sqlalchemy import (
    UUID,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .messages import MessageORM
    from .projects import ProjectORM


class ChatORM(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(
        String(255), nullable=False, server_default=text("'Новый чат'")
    )
    is_pinned: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    project: Mapped["ProjectORM | None"] = relationship(
        back_populates="chats", lazy="raise"
    )
    messages: Mapped[list["MessageORM"]] = relationship(
        back_populates="chat",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="raise",
        order_by="MessageModel.created_at",
    )

    __table_args__ = (
        CheckConstraint("length(trim(title)) > 0", name="title_not_empty"),
        Index("ix_chats_project_id_updated_at", "project_id", text("updated_at DESC")),
        Index(
            "ix_chats_standalone_updated_at",
            text("updated_at DESC"),
            postgresql_where=text("project_id IS NULL"),
        ),
        Index(
            "ix_chats_pinned_updated_at",
            text("updated_at DESC"),
            postgresql_where=text("is_pinned"),
        ),
    )
