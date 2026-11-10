from uuid import UUID

from app.application.schemas.entities.project import ProjectIdRead
from app.application.services.projects.base_project_services import BaseProjectServices
from app.domain.exceptions.project import ProjectNotFoundError


class DeleteProjectService(BaseProjectServices):
    async def __call__(self, project_id: UUID) -> ProjectIdRead:
        async with self.uow as uow:
            project = await uow.project.get(project_id)
            if project is None:
                self.logger.info(
                    "project.not_found", action="delete", project_id=str(project_id)
                )
                raise ProjectNotFoundError(project_id)
            project.mark_deleted()
            await uow.project.delete(project_id)
            await uow.commit()
        self.logger.info("project.deleted", project_id=str(project_id))
        return ProjectIdRead(project_id=project_id)
