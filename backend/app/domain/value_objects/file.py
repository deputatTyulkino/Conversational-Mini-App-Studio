from dataclasses import dataclass
from typing import Protocol


class IncomingFile(Protocol):
    @property
    def filename(self) -> str | None: ...

    @property
    def content_type(self) -> str | None: ...

    async def read(self, size: int = -1) -> bytes: ...


@dataclass(frozen=True, slots=True)
class StoredFile:
    relative_path: str
    stored_name: str
    original_name: str
    extension: str
    content_type: str | None
    size: int
