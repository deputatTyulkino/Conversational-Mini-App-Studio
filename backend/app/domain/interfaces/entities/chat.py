from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.chat import ChatDomain


class IChatRepo(ABC):
    @abstractmethod
    async def add(self, chat: ChatDomain) -> None: ...

    @abstractmethod
    async def get(self, chat_id: UUID) -> ChatDomain | None: ...

    @abstractmethod
    async def update(self, chat: ChatDomain) -> None: ...

    @abstractmethod
    async def delete(self, chat_id: UUID) -> None: ...

    @abstractmethod
    async def exists(self, chat_id: UUID) -> bool: ...

    @abstractmethod
    async def list_standalone(self) -> list[ChatDomain]: ...

    @abstractmethod
    async def list_pinned(self) -> list[ChatDomain]: ...
