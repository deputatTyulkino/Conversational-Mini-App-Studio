from typing import Annotated

from app.application.services.attachments.command.create_attachment import (
    CreateAttachmentService,
)
from app.domain.interfaces.storage.file_storage import IFileStorage
from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger
from app.infrastructure.dependencies.storage.file_storage import get_file_storage
from app.infrastructure.dependencies.uow.uow_depends import get_uow
from app.infrastructure.logging.logger import get_logger
from fastapi import Depends


def create_attachment_service(
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
    logger: Annotated[ILogger, Depends(get_logger)],
    file_storage: Annotated[IFileStorage, Depends(get_file_storage)],
) -> CreateAttachmentService:
    return CreateAttachmentService(uow, logger, file_storage)
