from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.domain.entities.message import MessageDomain


class IMessageRepo(ABC):
    @abstractmethod
    async def add(self, message: MessageDomain) -> None: ...

    @abstractmethod
    async def get(self, message_id: UUID) -> MessageDomain | None: ...

    @abstractmethod
    async def update(self, message: MessageDomain) -> None: ...

    @abstractmethod
    async def exists(self, message_id: UUID) -> bool: ...

    @abstractmethod
    async def list_by_chat(
        self,
        chat_id: UUID,
        limit: int,
        before_created_at: datetime | None = None,
        before_id: UUID | None = None,
    ) -> list[MessageDomain]: ...
