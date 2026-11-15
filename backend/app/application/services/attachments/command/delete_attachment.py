from uuid import UUID

from app.application.schemas.entities.attachment import AttachmentIdRead
from app.application.services.attachments.base_attachment_service import (
    BaseAttachmentService,
)
from app.domain.exceptions.attachment import (
    AttachmentAlreadySentError,
    AttachmentNotAvailableError,
    AttachmentNotFoundError,
)
from app.domain.exceptions.file import FileDeleteError


class DeleteAttachmentService(BaseAttachmentService):
    async def __call__(self, attachment_id: UUID) -> AttachmentIdRead:
        async with self.uow as uow:
            attachment = await uow.attachment.get(attachment_id)
            if attachment is None:
                raise AttachmentNotFoundError(attachment_id)
            if attachment.message_id is not None:
                raise AttachmentAlreadySentError(attachment_id)
            relative_path = await uow.attachment.delete_unattached(attachment_id)
            if relative_path is None:
                raise AttachmentNotAvailableError([attachment_id])
            await uow.commit()
        try:
            await self.file_storage.delete(relative_path)
        except FileDeleteError:
            self.logger.warning(
                "attachment.file_left_on_disk", attachment_id=str(attachment_id)
            )
        self.logger.info("attachment.deleted", attachment_id=str(attachment_id))
        return AttachmentIdRead(attachment_id=attachment_id)
