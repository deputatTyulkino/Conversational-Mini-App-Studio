from uuid import UUID

from app.application.schemas.common import ReadSchema


class AttachmentRead(ReadSchema):
    id: UUID
    original_name: str
    extension: str
    content_type: str | None
    size: int


class AttachmentIdRead(ReadSchema):
    attachment_id: UUID
