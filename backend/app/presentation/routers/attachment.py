from typing import Annotated
from urllib.parse import quote
from uuid import UUID

from app.application.schemas.entities.attachment import AttachmentIdRead
from app.application.services.attachments.command.create_attachment import (
    CreateAttachmentService,
)
from app.application.services.attachments.command.delete_attachment import (
    DeleteAttachmentService,
)
from app.application.services.attachments.queries.get_attachment import (
    GetAttachmentService,
)
from app.infrastructure.dependencies.entities.attachments.command.create_attachment import (
    create_attachment_service,
)
from app.infrastructure.dependencies.entities.attachments.command.delete_attachment import (
    delete_attachment_service,
)
from app.infrastructure.dependencies.entities.attachments.queries.get_attachment import (
    get_attachment_service,
)
from app.presentation.api.schemas.responses import SuccessResponse
from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api/attachments", tags=["attachments"])


@router.get("/{attachment_id}", response_model=None, status_code=status.HTTP_200_OK)
async def get_attachment_endpoint(
    attachment_id: UUID,
    get_attachment: Annotated[GetAttachmentService, Depends(get_attachment_service)],
):
    download = await get_attachment(attachment_id)
    return StreamingResponse(
        download.stream,
        media_type=download.content_type,
        headers={
            "Content-Disposition": (
                f"attachment; filename*=UTF-8''{quote(download.original_name)}"
            ),
            "Content-Length": str(download.size),
            "X-Content-Type-Options": "nosniff",
        },
    )


@router.post(
    "",
    response_model=SuccessResponse[AttachmentIdRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_attachment_endpoint(
    chat_id: Annotated[UUID, Query()],
    file: Annotated[UploadFile, File()],
    create_attachment: Annotated[
        CreateAttachmentService, Depends(create_attachment_service)
    ],
):
    data = await create_attachment(chat_id, file)
    return SuccessResponse(data=data)


@router.delete(
    "/{attachment_id}",
    response_model=SuccessResponse[AttachmentIdRead],
    status_code=status.HTTP_200_OK,
)
async def delete_attachment_endpoint(
    attachment_id: UUID,
    delete_attachment: Annotated[
        DeleteAttachmentService, Depends(delete_attachment_service)
    ],
):
    data = await delete_attachment(attachment_id)
    return SuccessResponse(data=data)
