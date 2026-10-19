from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.chat import ChatDomain


class IChat(ABC):
    @abstractmethod
    async def add(self, chat: ChatDomain) -> UUID: ...

    @abstractmethod
    async def get(self, chat_id: UUID) -> ChatDomain | None: ...

    @abstractmethod
    async def update(self, chat: ChatDomain) -> UUID: ...

    @abstractmethod
    async def delete(self, chat_id: UUID) -> UUID: ...

    @abstractmethod
    async def exists(self, chat_id: UUID) -> bool: ...

    @abstractmethod
    async def list_by_project(self, project_id: UUID) -> list[ChatDomain]: ...

    @abstractmethod
    async def list_standalone(self) -> list[ChatDomain]: ...

    @abstractmethod
    async def list_pinned(self) -> list[ChatDomain]: ...
