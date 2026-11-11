from typing import Annotated
from uuid import UUID

from app.application.schemas.entities.message import (
    MessageCreate,
    MessageListParams,
    MessagePage,
    MessageUpdate,
    SendMessageResponse,
)
from app.application.services.messages.command.create_message import (
    CreateMessageService,
)
from app.application.services.messages.command.update_message import (
    UpdateMessageService,
)
from app.application.services.messages.queries.get_all_messages import (
    GetAllMessagesService,
)
from app.infrastructure.dependencies.entities.messages.command.create_message import (
    create_message_service,
)
from app.infrastructure.dependencies.entities.messages.command.update_mesage import (
    update_message_service,
)
from app.infrastructure.dependencies.entities.messages.queries.get_messages import (
    get_messages_service,
)
from app.presentation.api.schemas.responses import SuccessResponse
from fastapi import APIRouter, Depends, File, Query, UploadFile, status

router = APIRouter(prefix="/{chat_id}/messages")


@router.get(
    "/",
    response_model=SuccessResponse[MessagePage],
    status_code=status.HTTP_200_OK,
    tags=["messages"],
)
async def get_messages(
    chat_id: UUID,
    params: Annotated[MessageListParams, Query()],
    get_messages_service: Annotated[
        GetAllMessagesService, Depends(get_messages_service)
    ],
):
    data = await get_messages_service(chat_id, params)
    return SuccessResponse(data=data)


@router.post(
    "/",
    response_model=SuccessResponse[SendMessageResponse],
    status_code=status.HTTP_201_CREATED,
    tags=["messages"],
)
async def create_message(
    chat_id: UUID,
    message_data: MessageCreate,
    create_message_service: Annotated[
        CreateMessageService, Depends(create_message_service)
    ],
    files: Annotated[list[UploadFile], File()],
):
    data = await create_message_service(chat_id, message_data, files)
    return SuccessResponse(data=data)


@router.patch(
    "/{message_id}",
    response_model=SuccessResponse[SendMessageResponse],
    status_code=status.HTTP_200_OK,
    tags=["messages"],
)
async def update_message(
    chat_id: UUID,
    message_id: UUID,
    message_data: MessageUpdate,
    update_message_service: Annotated[
        UpdateMessageService, Depends(update_message_service)
    ],
    files: Annotated[list[UploadFile], File()],
):
    data = await update_message_service(chat_id, message_id, message_data)
    return SuccessResponse(data=data)
