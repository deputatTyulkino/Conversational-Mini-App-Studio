from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.project import ProjectDomain


class IProjectRepo(ABC):
    @abstractmethod
    async def add(self, project: ProjectDomain) -> None: ...

    @abstractmethod
    async def get(self, project_id: UUID) -> ProjectDomain | None: ...

    @abstractmethod
    async def update(self, project: ProjectDomain) -> UUID: ...

    @abstractmethod
    async def delete(self, project_id: UUID) -> UUID: ...

    @abstractmethod
    async def exists(self, project_id: UUID) -> bool: ...

    @abstractmethod
    async def list_all(self) -> list[ProjectDomain]: ...
