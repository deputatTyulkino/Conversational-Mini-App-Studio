from typing import Annotated

from app.application.services.chats.queries.get_all_chats import (
    GetPinnedChatsService,
    GetStandaloneChatsService,
)
from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger
from app.infrastructure.dependencies.uow.uow_depends import get_uow
from app.infrastructure.logging.logger import get_logger
from fastapi import Depends


def get_pined_chats_service(
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
    logger: Annotated[ILogger, Depends(get_logger)],
) -> GetPinnedChatsService:
    return GetPinnedChatsService(uow, logger)


def get_standalone_chats_service(
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
    logger: Annotated[ILogger, Depends(get_logger)],
) -> GetStandaloneChatsService:
    return GetStandaloneChatsService(uow, logger)
