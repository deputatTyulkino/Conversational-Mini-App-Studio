from typing import Any
from uuid import UUID

from app.application.schemas.entities.attachment import AttachmentRead
from app.application.services.attachments.base_attachment_service import (
    BaseAttachmentService,
)
from app.domain.entities.attachment import AttachmentDomain
from app.domain.value_objects.file import IncomingFile


class CreateAttachmentService(BaseAttachmentService):
    async def __call__(
        self, chat_id: UUID | None, file: IncomingFile
    ) -> AttachmentRead:
        param: dict[Any, Any] = {"file": file}
        if chat_id is not None:
            param["namespace"] = chat_id
        saved_file = await self.file_storage.save(**param)
        attachment = AttachmentDomain.create(
            chat_id=chat_id,
            relative_path=saved_file.relative_path,
            stored_name=saved_file.stored_name,
            original_name=saved_file.original_name,
            content_type=saved_file.content_type,
            extension=saved_file.extension,
            size=saved_file.size,
        )
        try:
            async with self.uow as uow:
                await uow.attachment.add(attachment)
                await uow.commit()
        except BaseException:
            await self.file_storage.delete(saved_file.relative_path)
            raise
        self.logger.info(
            "attachment.created",
            attachment_id=str(attachment.id),
            size=attachment.size,
        )
        return AttachmentRead.model_validate(attachment)
