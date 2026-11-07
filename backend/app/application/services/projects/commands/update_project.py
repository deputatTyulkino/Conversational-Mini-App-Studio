from uuid import UUID

from app.application.schemas.entities.project import ProjectUpdate
from app.application.services.projects.base_project_services import BaseProjectServcies
from app.domain.exceptions.project import ProjectNotFoundError


class UpdateProjectService(BaseProjectServcies):
    async def __call__(
        self, project_id: UUID, project_data: ProjectUpdate
    ) -> dict[str, UUID]:
        async with self.uow as uow:
            project = await uow.project.get(project_id)
            if project is None:
                raise ProjectNotFoundError(project_id)
            if project_data.name is not None:
                project.rename(project_data.name)
            if project_data.description is not None:
                project.change_description(project_data.description)
            updated_project_id = await uow.project.update(project)
            await uow.commit()
        return {"project_id": updated_project_id}
