from app.domain.interfaces.storage.file_storage import IFileStorage
from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger


class BaseAttachmentService:
    def __init__(self, uow: IUnitOfWork, logger: ILogger, file_storage: IFileStorage):
        self.uow = uow
        self.logger = logger
        self.file_storage = file_storage
