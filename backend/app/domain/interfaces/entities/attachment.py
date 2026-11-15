from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from app.domain.entities.attachment import AttachmentDomain


class IAttachmentRepo(ABC):
    @abstractmethod
    async def add(self, attachment: AttachmentDomain) -> None: ...

    @abstractmethod
    async def get(self, attachment_id: UUID) -> AttachmentDomain | None: ...

    @abstractmethod
    async def attach_to_message(
        self, chat_id: UUID, message_id: UUID, attachment_ids: Sequence[UUID]
    ) -> list[AttachmentDomain]: ...

    @abstractmethod
    async def delete_from_message(
        self, message_id: UUID, attachment_ids: Sequence[UUID]
    ) -> list[str]: ...

    @abstractmethod
    async def delete_unattached(self, attachment_id: UUID) -> str | None: ...
