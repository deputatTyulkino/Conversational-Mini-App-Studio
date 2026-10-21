from uuid import UUID

from app.application.services.projects.base_project_services import BaseProjectServcies
from app.domain.exceptions.project import ProjectNotFoundError


class DeleteProjectService(BaseProjectServcies):
    async def __call__(self, project_id: UUID) -> dict[str, UUID]:
        async with self.uow as uow:
            exists_project = await uow.project.exists(project_id)
            if not exists_project:
                raise ProjectNotFoundError(project_id)
            deleted_project_id = await uow.project.delete(project_id)
        return {"project_id": deleted_project_id}
