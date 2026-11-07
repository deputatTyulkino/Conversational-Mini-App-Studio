from typing import Annotated

from app.application.services.messages.command.update_message import (
    UpdateMessageService,
)
from app.application.services.tool_router.tool_router_service import ToolRouterService
from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger
from app.infrastructure.dependencies.uow.uow_depends import get_uow
from app.infrastructure.logging.logger import get_logger
from fastapi import Depends


def update_message_service(
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
    logger: Annotated[ILogger, Depends(get_logger)],
) -> UpdateMessageService:
    tool_router = ToolRouterService()
    return UpdateMessageService(uow, logger, tool_router)
