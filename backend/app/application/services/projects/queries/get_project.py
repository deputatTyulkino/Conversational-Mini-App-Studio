from uuid import UUID

from app.application.schemas.entities.project import ProjectWithChatsRead
from app.application.services.projects.base_project_services import BaseProjectServices
from app.domain.exceptions.project import ProjectNotFoundError


class GetProjectService(BaseProjectServices):
    async def __call__(self, project_id: UUID) -> ProjectWithChatsRead:
        async with self.uow as uow:
            project = await uow.project.get_with_chats(project_id)
            if project is None:
                self.logger.info(
                    "project.not_found", action="get", project_id=str(project_id)
                )
                raise ProjectNotFoundError(project_id)
        self.logger.debug(
            "project.fetched", project_id=str(project_id), chats=len(project.chats)
        )
        return ProjectWithChatsRead.model_validate(project)
