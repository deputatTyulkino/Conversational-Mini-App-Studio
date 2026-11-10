from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger


class BaseProjectServices:
    def __init__(self, uow: IUnitOfWork, logger: ILogger):
        self.uow = uow
        self.logger = logger
