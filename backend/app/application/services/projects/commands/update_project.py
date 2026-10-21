from uuid import UUID

from app.application.schemas.project import ProjectUpdate
from app.application.services.projects.base_project_services import BaseProjectServcies
from app.domain.entities.project import ProjectDomain
from app.domain.exceptions.project import ProjectNotFoundError


class UpdateProjectService(BaseProjectServcies):
    async def __call__(
        self, project_id: UUID, project_data: ProjectUpdate
    ) -> dict[str, UUID]:
        async with self.uow as uow:
            exists_project = await uow.project.exists(project_id)
            if not exists_project:
                raise ProjectNotFoundError(project_id)
            updated_project_id = await uow.project.update(
                ProjectDomain(project_id, **project_data.model_dump())
            )
        return {"project_id": updated_project_id}
