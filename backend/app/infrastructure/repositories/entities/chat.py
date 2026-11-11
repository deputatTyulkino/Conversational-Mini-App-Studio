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

    @staticmethod
    def _to_domain_model(chat: ChatORM) -> ChatDomain:
        return ChatDomain(
            id=chat.id,
            title=chat.title,
            project_id=chat.project_id,
            is_pinned=chat.is_pinned,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
        )

    @staticmethod
    def _to_orm_model(chat: ChatDomain) -> ChatORM:
        return ChatORM(
            id=chat.id,
            title=chat.title,
            project_id=chat.project_id,
            is_pinned=chat.is_pinned,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
        )

    async def add(self, chat: ChatDomain) -> None:
        self.session.add(self._to_orm_model(chat))
        await self.session.flush()
        self.logger.debug("chat_repo.add", chat_id=str(chat.id))

    async def get(self, chat_id: UUID) -> ChatDomain | None:
        query = select(ChatORM).filter(ChatORM.id == chat_id)
        chat = (await self.session.execute(query)).scalar_one_or_none()
        if chat is None:
            return None
        return self._to_domain_model(chat)

    async def update(self, chat: ChatDomain) -> None:
        stmt = (
            update(ChatORM)
            .filter(ChatORM.id == chat.id)
            .values(
                title=chat.title,
                project_id=chat.project_id,
                is_pinned=chat.is_pinned,
                updated_at=chat.updated_at,
            )
            .returning(ChatORM.id)
        )
        updated_id = (await self.session.execute(stmt)).scalar_one_or_none()
        if updated_id is None:
            self.logger.warning("chat_repo.update_no_rows", chat_id=str(chat.id))
            return
        self.logger.debug("chat_repo.update", chat_id=str(chat.id))

    async def delete(self, chat_id: UUID) -> None:
        stmt = delete(ChatORM).filter(ChatORM.id == chat_id).returning(ChatORM.id)
        deleted_id = (await self.session.execute(stmt)).scalar_one_or_none()
        if deleted_id is None:
            self.logger.warning("chat_repo.delete_no_rows", chat_id=str(chat_id))
            return
        self.logger.debug("chat_repo.delete", chat_id=str(chat_id))

    async def exists(self, chat_id: UUID) -> bool:
        query = select(exists(ChatORM).where(ChatORM.id == chat_id))
        return (await self.session.execute(query)).scalar_one()

    async def list_standalone(self) -> list[ChatDomain]:
        query = (
            select(ChatORM)
            .filter(ChatORM.is_pinned.is_(False), ChatORM.project_id.is_(None))
            .order_by(ChatORM.updated_at.desc(), ChatORM.id)
        )
        chats = (await self.session.scalars(query)).all()
        self.logger.debug("chat_repo.list_standalone", count=len(chats))
        return [self._to_domain_model(chat) for chat in chats]

    async def list_pinned(self) -> list[ChatDomain]:
        query = (
            select(ChatORM)
            .filter(ChatORM.is_pinned)
            .order_by(ChatORM.updated_at.desc(), ChatORM.id)
        )
        chats = (await self.session.scalars(query)).all()
        self.logger.debug("chat_repo.list_pinned", count=len(chats))
        return [self._to_domain_model(chat) for chat in chats]
