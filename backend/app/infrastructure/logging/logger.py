# infrastructure/logging/structlog_logger.py
from __future__ import annotations

from typing import Any

import structlog
from app.domain.logging.i_logger import ILogger


class StructlogLogger(ILogger):
    def __init__(self, logger: structlog.stdlib.BoundLogger) -> None:
        self._logger = logger

    def bind(self, **context: Any) -> StructlogLogger:
        return StructlogLogger(self._logger.bind(**context))

    def debug(self, event: str, **kwargs: Any) -> None:
        self._logger.debug(event, **kwargs)

    def info(self, event: str, **kwargs: Any) -> None:
        self._logger.info(event, **kwargs)

    def warning(self, event: str, **kwargs: Any) -> None:
        self._logger.warning(event, **kwargs)

    def error(self, event: str, **kwargs: Any) -> None:
        self._logger.error(event, **kwargs)

    def exception(self, event: str, **kwargs: Any) -> None:
        self._logger.exception(event, **kwargs)


def get_logger(name: str) -> ILogger:
    return StructlogLogger(structlog.stdlib.get_logger(name))
