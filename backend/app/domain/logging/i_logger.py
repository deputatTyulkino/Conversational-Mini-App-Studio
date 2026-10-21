from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ILogger(ABC):
    @abstractmethod
    def bind(self, **context: Any) -> ILogger: ...

    @abstractmethod
    def debug(self, event: str, **kwargs: Any) -> None: ...

    @abstractmethod
    def info(self, event: str, **kwargs: Any) -> None: ...

    @abstractmethod
    def warning(self, event: str, **kwargs: Any) -> None: ...

    @abstractmethod
    def error(self, event: str, **kwargs: Any) -> None: ...

    @abstractmethod
    def exception(self, event: str, **kwargs: Any) -> None: ...
