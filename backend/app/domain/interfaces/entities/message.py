from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.message import MessageDomain


class IMessageRepo(ABC):
    @abstractmethod
    async def add(self, message: MessageDomain) -> UUID: ...

    @abstractmethod
    async def get(self, message_id: UUID) -> MessageDomain | None: ...

    @abstractmethod
    async def list_by_chat(
        self,
        chat_id: UUID,
        *,
        limit: int | None = None,
        before_id: UUID | None = None,
    ) -> list[MessageDomain]: ...

    @abstractmethod
    async def delete(self, message_id: UUID) -> UUID: ...
