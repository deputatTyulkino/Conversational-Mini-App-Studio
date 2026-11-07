from uuid import UUID

from app.application.services.projects.base_project_services import BaseProjectServcies
from app.domain.exceptions.project import ProjectNotFoundError


class DeleteProjectService(BaseProjectServcies):
    async def __call__(self, project_id: UUID) -> dict[str, UUID]:
        async with self.uow as uow:
            project = await uow.project.get(project_id)
            if project is None:
                raise ProjectNotFoundError(project_id)
            project.mark_deleted()
            deleted_project_id = await uow.project.delete(project_id)
            await uow.commit()
        return {"project_id": deleted_project_id}
