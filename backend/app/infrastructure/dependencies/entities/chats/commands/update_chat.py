from typing import Annotated

from app.application.services.chats.commands.update_chat import UpdateChatService
from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger
from app.infrastructure.dependencies.uow.uow_depends import get_uow
from app.infrastructure.logging.logger import get_logger
from fastapi import Depends


def update_chat_servcice(
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
    logger: Annotated[ILogger, Depends(get_logger)],
) -> UpdateChatService:
    return UpdateChatService(uow, logger)
