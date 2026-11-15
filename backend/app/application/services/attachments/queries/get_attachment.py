from collections.abc import AsyncIterator
from dataclasses import dataclass
from uuid import UUID

from app.application.services.attachments.base_attachment_service import (
    BaseAttachmentService,
)
from app.domain.exceptions.attachment import AttachmentNotFoundError


@dataclass(frozen=True, slots=True)
class AttachmentDownload:
    stream: AsyncIterator[bytes]
    original_name: str
    content_type: str
    size: int


class GetAttachmentService(BaseAttachmentService):
    async def __call__(self, attachment_id: UUID) -> AttachmentDownload:
        async with self.uow as uow:
            attachment = await uow.attachment.get(attachment_id)
            if attachment is None:
                raise AttachmentNotFoundError(attachment_id)
        stream = await self.file_storage.open_stream(attachment.relative_path)
        self.logger.debug(
            "attachment.download_started", attachment_id=str(attachment_id)
        )
        return AttachmentDownload(
            stream=stream,
            original_name=attachment.original_name,
            content_type=attachment.content_type or "application/octet-stream",
            size=attachment.size,
        )
