from typing import Annotated

from app.application.services.projects.commands.delete_project import (
    DeleteProjectService,
)
from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger
from app.infrastructure.dependencies.uow.uow_depends import get_uow
from app.infrastructure.logging.logger import get_logger
from fastapi import Depends


def delete_project_service(
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
    logger: Annotated[ILogger, Depends(get_logger)],
) -> DeleteProjectService:
    return DeleteProjectService(uow, logger)
