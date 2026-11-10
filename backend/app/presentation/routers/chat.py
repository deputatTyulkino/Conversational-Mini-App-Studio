from typing import Annotated
from uuid import UUID

from app.application.schemas.entities.chat import ChatCreate, ChatRead, ChatUpdate
from app.application.services.chats.commands.create_chat import CreateChatService
from app.application.services.chats.commands.delete_chat import DeleteChatService
from app.application.services.chats.commands.update_chat import UpdateChatService
from app.application.services.chats.queries.get_all_chats import (
    GetPinedChatsService,
    GetStanaloneChatsService,
)
from app.application.services.chats.queries.get_chat import GetChatService
from app.domain.exceptions.chat import ChatNotFoundError
from app.infrastructure.dependencies.entities.chats.commands.create_chat import (
    create_chat_servcice,
)
from app.infrastructure.dependencies.entities.chats.commands.delete_chat import (
    delete_chat_servcice,
)
from app.infrastructure.dependencies.entities.chats.commands.update_chat import (
    update_chat_servcice,
)
from app.infrastructure.dependencies.entities.chats.queries.get_all_chats import (
    get_pined_chats_service,
    get_standalone_chats_service,
)
from app.infrastructure.dependencies.entities.chats.queries.get_chats import (
    get_chat_service,
)
from app.presentation.api.exceptions.chat import ChatNotFoundHTTPException
from app.presentation.api.schemas.responses import SuccessResponse
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/api/chats")


@router.get(
    "/pined",
    response_model=SuccessResponse[list[ChatRead]],
    status_code=status.HTTP_200_OK,
    tags=["chats"],
)
async def get_pined_chats(
    pined_chats_service: Annotated[
        GetPinedChatsService, Depends(get_pined_chats_service)
    ],
):
    data = await pined_chats_service()
    return SuccessResponse(data=data)


@router.get(
    "/standalone",
    response_model=SuccessResponse[list[ChatRead]],
    status_code=status.HTTP_200_OK,
    tags=["chats"],
)
async def get_standalone_chats(
    standalone_chats_service: Annotated[
        GetStanaloneChatsService, Depends(get_standalone_chats_service)
    ],
):
    data = await standalone_chats_service()
    return SuccessResponse(data=data)


@router.get(
    "/{chat_id}",
    response_model=SuccessResponse[ChatRead],
    status_code=status.HTTP_200_OK,
    tags=["chats"],
)
async def get_chat(
    chat_id: UUID,
    get_chat_service: Annotated[GetChatService, Depends(get_chat_service)],
):
    try:
        data = await get_chat_service(chat_id)
    except ChatNotFoundError as e:
        raise ChatNotFoundHTTPException(str(e), code=e.code)
    return SuccessResponse(data=data)


@router.post(
    "",
    response_model=SuccessResponse[dict[str, UUID]],
    status_code=status.HTTP_201_CREATED,
    tags=["chats"],
)
async def create_chat(
    chat_data: ChatCreate,
    create_chat_service: Annotated[CreateChatService, Depends(create_chat_servcice)],
):
    data = await create_chat_service(chat_data)
    return SuccessResponse(data=data)


@router.patch(
    "/{chat_id}",
    response_model=SuccessResponse[dict[str, UUID]],
    status_code=status.HTTP_200_OK,
    tags=["chats"],
)
async def update_chat(
    chat_id: UUID,
    chat_data: ChatUpdate,
    update_chat_service: Annotated[UpdateChatService, Depends(update_chat_servcice)],
):
    try:
        data = await update_chat_service(chat_id, chat_data)
    except ChatNotFoundError as e:
        raise ChatNotFoundHTTPException(str(e), code=e.code)
    return SuccessResponse(data=data)


@router.delete(
    "/{chat_id}",
    response_model=SuccessResponse[dict[str, UUID]],
    status_code=status.HTTP_200_OK,
    tags=["chats"],
)
async def delete_chat(
    chat_id: UUID,
    delete_chat_service: Annotated[DeleteChatService, Depends(delete_chat_servcice)],
):
    try:
        data = await delete_chat_service(chat_id)
    except ChatNotFoundError as e:
        raise ChatNotFoundHTTPException(str(e), code=e.code)
    return SuccessResponse(data=data)
