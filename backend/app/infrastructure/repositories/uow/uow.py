from types import TracebackType
from typing import Self

from app.domain.interfaces.entities.chat import IChat
from app.domain.interfaces.entities.message import IMessage
from app.domain.interfaces.entities.project import IProject
from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class UnitOfWork(IUnitOfWork):
    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession], logger: ILogger
    ):
        self.logger = logger
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self.message: IMessage | None = None
        self.chat: IChat | None = None
        self.project: IProject | None = None

    async def __aenter__(self) -> Self:
        if self.session is not None:
            raise RuntimeError("UnitOfWork уже активен")
        self.session = self.session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
        finally:
            if self.session:
                await self.session.close()
            self.session = None

    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork не инициализирован")
        await self.session.commit()

    async def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork не инициализирован")
        await self.session.rollback()
