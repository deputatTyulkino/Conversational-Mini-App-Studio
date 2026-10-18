from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.message import Message


class MessageRepository(ABC):
    @abstractmethod
    async def add(self, message: Message) -> None: ...

    @abstractmethod
    async def get(self, message_id: UUID) -> Message | None: ...

    @abstractmethod
    async def list_by_chat(
        self,
        chat_id: UUID,
        *,
        limit: int | None = None,
        before_id: UUID | None = None,
    ) -> list[Message]: ...

    @abstractmethod
    async def count_by_chat(self, chat_id: UUID) -> int: ...

    @abstractmethod
    async def delete(self, message: Message) -> None: ...
