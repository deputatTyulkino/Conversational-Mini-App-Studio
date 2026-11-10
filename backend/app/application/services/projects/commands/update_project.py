from uuid import UUID

from app.application.schemas.entities.project import ProjectIdRead, ProjectUpdate
from app.application.services.projects.base_project_services import BaseProjectServices
from app.domain.exceptions.project import ProjectNotFoundError


class UpdateProjectService(BaseProjectServices):
    async def __call__(
        self, project_id: UUID, project_data: ProjectUpdate
    ) -> ProjectIdRead:
        async with self.uow as uow:
            project = await uow.project.get(project_id)
            if project is None:
                self.logger.info(
                    "project.not_found", action="update", project_id=str(project_id)
                )
                raise ProjectNotFoundError(project_id)
            changes = project_data.model_dump(exclude_unset=True)
            if "name" in changes:
                project.rename(changes["name"])
            if "description" in changes:
                project.change_description(changes["description"])
            await uow.project.update(project)
            await uow.commit()
        self.logger.info(
            "project.updated",
            project_id=str(project_id),
            requested_fields=sorted(changes),
        )
        return ProjectIdRead(project_id=project_id)
