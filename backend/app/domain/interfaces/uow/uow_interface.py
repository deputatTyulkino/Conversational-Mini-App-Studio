import logging
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from app.domain.interfaces.entities.chat import IChatRepo
from app.domain.interfaces.entities.message import IMessageRepo
from app.domain.interfaces.entities.project import IProjectRepo

logger = logging.getLogger(__name__)


class IUnitOfWork(ABC):
    @property
    @abstractmethod
    def chat(sellf) -> IChatRepo: ...

    @property
    @abstractmethod
    def message(self) -> IMessageRepo: ...

    @property
    @abstractmethod
    def project(self) -> IProjectRepo: ...

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
