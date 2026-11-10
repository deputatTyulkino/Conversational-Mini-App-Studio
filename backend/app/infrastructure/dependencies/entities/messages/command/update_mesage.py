from typing import Annotated

from app.application.services.messages.command.update_message import (
    UpdateMessageService,
)
from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger
from app.infrastructure.dependencies.uow.uow_depends import get_uow
from app.infrastructure.logging.logger import get_logger
from fastapi import Depends, Request


def update_message_service(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
    logger: Annotated[ILogger, Depends(get_logger)],
) -> UpdateMessageService:
    return UpdateMessageService(uow, logger, request.app.state.tool_router)
