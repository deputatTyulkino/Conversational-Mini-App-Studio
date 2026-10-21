from typing import Annotated

from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger
from app.infrastructure.logging.logger import get_logger
from app.infrastructure.repositories.uow.uow import UnitOfWork
from fastapi import Depends, Request


def get_uow(
    request: Request, logger: Annotated[ILogger, Depends(get_logger)]
) -> IUnitOfWork:
    return UnitOfWork(request.state.session_factory, logger)
