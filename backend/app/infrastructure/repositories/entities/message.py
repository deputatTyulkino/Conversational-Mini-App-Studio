from datetime import datetime
from uuid import UUID

from app.domain.entities.attachment import AttachmentDomain
from app.domain.entities.message import MessageDomain
from app.domain.interfaces.entities.message import IMessageRepo
from app.domain.logging.i_logger import ILogger
from app.infrastructure.db.models.attachments import AttachmentORM
from app.infrastructure.db.models.messages import MessageORM
from sqlalchemy import exists, select, tuple_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class MessageRepo(IMessageRepo):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self.session = session
        self.logger = logger

    @staticmethod
    def _to_attachment_domain_model(attachment: AttachmentORM) -> AttachmentDomain:
        return AttachmentDomain(
            id=attachment.id,
            chat_id=attachment.chat_id,
            message_id=attachment.message_id,
            stored_name=attachment.stored_name,
            relative_path=attachment.relative_path,
            original_name=attachment.original_name,
            content_type=attachment.content_type,
            extension=attachment.extension,
            size=attachment.size,
            created_at=attachment.created_at,
        )

    def _to_domain_model(self, message: MessageORM) -> MessageDomain:
        return MessageDomain(
            id=message.id,
            chat_id=message.chat_id,
            role=message.role,
            content=message.content,
            payload=message.payload,
            created_at=message.created_at,
            attachments=[
                self._to_attachment_domain_model(at) for at in message.attachments
            ],
        )

    @staticmethod
    def _to_orm_model(message: MessageDomain) -> MessageORM:
        return MessageORM(
            id=message.id,
            chat_id=message.chat_id,
            role=message.role,
            content=message.content,
            payload=message.payload,
            created_at=message.created_at,
        )

    async def add(self, message: MessageDomain) -> None:
        self.session.add(self._to_orm_model(message))
        await self.session.flush()
        self.logger.debug("message_repo.add", message_id=str(message.id))

    async def get(self, message_id: UUID) -> MessageDomain | None:
        query = (
            select(MessageORM)
            .filter(MessageORM.id == message_id)
            .options(selectinload(MessageORM.attachments))
        )
        message = (await self.session.execute(query)).scalar_one_or_none()
        if message is None:
            return None
        return self._to_domain_model(message)

    async def update(self, message: MessageDomain) -> None:
        stmt = (
            update(MessageORM)
            .filter(MessageORM.id == message.id)
            .values(content=message.content)
            .returning(MessageORM.id)
        )
        updated_id = (await self.session.execute(stmt)).scalar_one_or_none()
        if updated_id is None:
            self.logger.warning(
                "message_repo.update_no_rows", message_id=str(message.id)
            )
            return
        self.logger.debug("message_repo.update", message_id=str(message.id))

    async def exists(self, message_id: UUID) -> bool:
        query = select(exists(MessageORM).where(MessageORM.id == message_id))
        return (await self.session.execute(query)).scalar_one()

    async def list_by_chat(
        self,
        chat_id: UUID,
        limit: int,
        before_created_at: datetime | None = None,
        before_id: UUID | None = None,
    ) -> list[MessageDomain]:
        query = (
            select(MessageORM)
            .filter(MessageORM.chat_id == chat_id)
            .options(selectinload(MessageORM.attachments))
        )
        if before_created_at is not None and before_id is not None:
            query = query.filter(
                tuple_(MessageORM.created_at, MessageORM.id)
                < (before_created_at, before_id)
            )
        query = query.order_by(
            MessageORM.created_at.desc(), MessageORM.id.desc()
        ).limit(limit + 1)
        messages = (await self.session.scalars(query)).all()
        self.logger.debug(
            "message_repo.list_by_chat", chat_id=str(chat_id), count=len(messages)
        )
        return [self._to_domain_model(message) for message in reversed(messages)]
