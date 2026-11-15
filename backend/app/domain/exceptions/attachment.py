from collections.abc import Iterable
from uuid import UUID

from app.domain.exceptions.base import NotFoundError

from .base import ConflictError


class AttachmentNotFoundError(NotFoundError):
    code = "attachment_not_found"

    def __init__(self, attachment_id: UUID | int | str | None = None) -> None:
        super().__init__(
            f"Attachment {attachment_id} not found"
            if attachment_id is not None
            else "Attachment not found",
            attachment_id=attachment_id,
        )


class AttachmentNotAvailableError(ConflictError):
    code = "attachment_not_available"

    def __init__(self, attachment_ids: Iterable[UUID]) -> None:
        ids = sorted(str(attachment_id) for attachment_id in attachment_ids)
        super().__init__(
            "Some attachments are not available for this message",
            attachment_ids=ids,
        )


class AttachmentAlreadySentError(ConflictError):
    code = "attachment_already_sent"

    def __init__(self, attachment_id: UUID) -> None:
        super().__init__(
            "Attachment is already attached to a message",
            attachment_id=attachment_id,
        )
