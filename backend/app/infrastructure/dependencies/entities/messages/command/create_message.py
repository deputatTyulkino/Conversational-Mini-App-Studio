from typing import Annotated

from app.application.services.messages.command.create_message import (
    CreateMessageService,
)
from app.application.services.tool_router.tool_router_service import ToolRouterService
from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger
from app.infrastructure.dependencies.uow.uow_depends import get_uow
from app.infrastructure.logging.logger import get_logger
from fastapi import Depends


def create_message_service(
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
    logger: Annotated[ILogger, Depends(get_logger)],
) -> CreateMessageService:
    tool_router = ToolRouterService()
    return CreateMessageService(uow, logger, tool_router)
