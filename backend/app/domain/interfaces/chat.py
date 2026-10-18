from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.chat import Chat


class ChatRepository(ABC):
    @abstractmethod
    async def add(self, chat: Chat) -> None: ...

    @abstractmethod
    async def get(self, chat_id: UUID) -> Chat | None: ...

    @abstractmethod
    async def update(self, chat: Chat) -> None: ...

    @abstractmethod
    async def delete(self, chat: Chat) -> None: ...

    @abstractmethod
    async def exists(self, chat_id: UUID) -> bool: ...

    @abstractmethod
    async def list_by_project(self, project_id: UUID) -> list[Chat]: ...

    @abstractmethod
    async def list_standalone(self) -> list[Chat]: ...

    @abstractmethod
    async def list_pinned(self) -> list[Chat]: ...
