import logging
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from app.domain.common import AggregateRoot

logger = logging.getLogger(__name__)


class UnitOfWork(ABC):
    async def __aenter__(self) -> Self: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...

    def track(self, aggregate: AggregateRoot) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...

    @abstractmethod
    async def _commit(self) -> None: ...

    @abstractmethod
    async def _rollback(self) -> None: ...
