from types import TracebackType
from typing import Self

from app.domain.interfaces.entities.chat import IChatRepo
from app.domain.interfaces.entities.message import IMessageRepo
from app.domain.interfaces.entities.project import IProjectRepo
from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger
from app.infrastructure.repositories.entities.chat import ChatRepo
from app.infrastructure.repositories.entities.message import MessageRepo
from app.infrastructure.repositories.entities.project import ProjectRepo
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class UnitOfWork(IUnitOfWork):
    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession], logger: ILogger
    ):
        self.logger = logger
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self._message: IMessageRepo | None = None
        self._chat: IChatRepo | None = None
        self._project: IProjectRepo | None = None

    @property
    def message(self) -> IMessageRepo:
        if self._message is None:
            raise RuntimeError("Unit of Work не инициализирован")
        return self._message

    @property
    def chat(self) -> IChatRepo:
        if self._chat is None:
            raise RuntimeError("Unit of Work не инициализирован")
        return self._chat

    @property
    def project(self) -> IProjectRepo:
        if self._project is None:
            raise RuntimeError("Unit of Work не инициализирован")
        return self._project

    async def __aenter__(self) -> Self:
        if self.session is not None:
            raise RuntimeError("UnitOfWork уже активен")
        self.session = self.session_factory()
        self._message = MessageRepo(self.session, self.logger)
        self._chat = ChatRepo(self.session, self.logger)
        self._project = ProjectRepo(self.session, self.logger)
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
            self._chat = None
            self._message = None
            self._project = None

    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork не инициализирован")
        await self.session.commit()

    async def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork не инициализирован")
        await self.session.rollback()
