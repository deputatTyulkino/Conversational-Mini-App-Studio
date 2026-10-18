from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.project import Project


class IProject(ABC):
    @abstractmethod
    async def add(self, project: Project) -> None: ...

    @abstractmethod
    async def get(self, project_id: UUID) -> Project | None: ...

    @abstractmethod
    async def update(self, project: Project) -> None: ...

    @abstractmethod
    async def delete(self, project: Project) -> None: ...

    @abstractmethod
    async def exists(self, project_id: UUID) -> bool: ...

    @abstractmethod
    async def list_all(self) -> list[Project]: ...
