from uuid import UUID

from app.domain.entities.message import MessageDomain
from app.domain.interfaces.entities.message import IMessage
from app.domain.logging.i_logger import ILogger
from app.infrastructure.db.models.messages import MessageORM
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class MessageRepo(IMessage):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self.session = session
        self.logger = logger

    def _to_domain_model(self, message: MessageORM) -> MessageDomain:
        return MessageDomain(
            id=message.id,
            chat_id=message.chat_id,
            role=message.role,
            content=message.content,
            payload=message.payload,
            created_at=message.created_at,
        )

    def _to_orm_model(self, message: MessageDomain) -> MessageORM:
        return MessageORM(
            id=message.id,
            chat_id=message.chat_id,
            role=message.role,
            content=message.content,
            payload=message.payload,
            created_at=message.created_at,
        )

    async def add(self, message: MessageDomain) -> UUID:
        new_message = self._to_orm_model(message)
        self.session.add(new_message)
        await self.session.flush()
        return new_message.id

    async def get(self, message_id: UUID) -> MessageDomain | None:
        query = select(MessageORM).filter(MessageORM.id == message_id)
        message = (await self.session.execute(query)).scalar_one_or_none()
        if message is None:
            return None
        return self._to_domain_model(message)

    async def list_by_chat(
        self, chat_id: UUID, *, limit: int | None = None, before_id: UUID | None = None
    ) -> list[MessageDomain]:
        filters = {}
        if limit is not None:
            filters["limit"] = limit
        if before_id is not None:
            query = (
                select(MessageORM)
                .filter(
                    MessageORM.chat_id == chat_id, MessageORM.id == before_id, **filters
                )
                .order_by(MessageORM.created_at.desc())
            )
        else:
            query = (
                select(MessageORM)
                .filter(MessageORM.chat_id == chat_id, **filters)
                .order_by(MessageORM.created_at)
            )
        messages = (await self.session.scalars(query)).all()
        return [self._to_domain_model(message) for message in messages]

    async def delete(self, message_id: UUID) -> UUID:
        stmt = (
            delete(MessageORM)
            .filter(MessageORM.id == message_id)
            .returning(MessageORM.id)
        )
        deleted_message_id = (await self.session.execute(stmt)).scalar_one()
        return deleted_message_id
