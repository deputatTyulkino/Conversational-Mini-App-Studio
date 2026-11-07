from uuid import UUID

from app.application.schemas.entities.project import ProjectWithChatsRead
from app.application.services.projects.base_project_services import BaseProjectServcies
from app.domain.exceptions.project import ProjectNotFoundError


class GetProjectService(BaseProjectServcies):
    async def __call__(self, project_id: UUID) -> ProjectWithChatsRead:
        async with self.uow as uow:
            project = await uow.project.get(project_id)
            if project is None:
                raise ProjectNotFoundError(project_id)
            chats = await uow.chat.list_by_project(project_id)
        return ProjectWithChatsRead.build(project, chats)
