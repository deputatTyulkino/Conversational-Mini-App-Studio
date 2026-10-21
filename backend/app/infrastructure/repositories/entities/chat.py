from uuid import UUID

from app.domain.entities.chat import ChatDomain
from app.domain.interfaces.entities.chat import IChatRepo
from app.domain.logging.i_logger import ILogger
from app.infrastructure.db.models.chats import ChatORM
from sqlalchemy import delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class ChatRepo(IChatRepo):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self.session = session
        self.logger = logger

    def _to_domain_model(self, chat: ChatORM) -> ChatDomain:
        return ChatDomain(
            id=chat.id,
            title=chat.title,
            project_id=chat.project_id,
            is_pinned=chat.is_pinned,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
        )

    def _to_orm_model(self, chat: ChatDomain) -> ChatORM:
        return ChatORM(
            id=chat.id,
            title=chat.title,
            project_id=chat.project_id,
            is_pinned=chat.is_pinned,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
        )

    async def add(self, chat: ChatDomain) -> None:
        new_chat = self._to_orm_model(chat)
        self.session.add(new_chat)
        await self.session.flush()

    async def get(self, chat_id: UUID) -> ChatDomain | None:
        query = select(ChatORM).filter(ChatORM.id == chat_id)
        chat = (await self.session.execute(query)).scalar_one_or_none()
        if chat is None:
            return None
        return self._to_domain_model(chat)

    async def update(self, chat: ChatDomain) -> UUID:
        stmt = (
            update(ChatORM)
            .filter(ChatORM.id == chat.id)
            .values(**chat.as_dict())
            .returning(ChatORM.id)
        )
        updated_chat_id = (await self.session.execute(stmt)).scalar_one()
        return updated_chat_id

    async def delete(self, chat_id: UUID) -> UUID:
        stmt = delete(ChatORM).filter(ChatORM.id == chat_id).returning(ChatORM.id)
        deleted_chat_id = (await self.session.execute(stmt)).scalar_one()
        return deleted_chat_id

    async def exists(self, chat_id: UUID) -> bool:
        query = select(exists(ChatORM).where(ChatORM.id == chat_id))
        exists_chat = (await self.session.execute(query)).scalar_one()
        return exists_chat

    async def list_by_project(self, project_id: UUID) -> list[ChatDomain]:
        query = select(ChatORM).filter(ChatORM.project_id == project_id)
        chats = (await self.session.scalars(query)).all()
        return [self._to_domain_model(chat) for chat in chats]

    async def list_standalone(self) -> list[ChatDomain]:
        query = select(ChatORM)
        chats = (await self.session.scalars(query)).all()
        return [self._to_domain_model(chat) for chat in chats]

    async def list_pinned(self) -> list[ChatDomain]:
        query = select(ChatORM).filter(ChatORM.is_pinned)
        chats = (await self.session.scalars(query)).all()
        return [self._to_domain_model(chat) for chat in chats]
