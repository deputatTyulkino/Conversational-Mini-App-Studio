from app.application.schemas.entities.project import ProjectWithChatsRead
from app.application.services.projects.base_project_services import BaseProjectServices


class GetAllProjectService(BaseProjectServices):
    async def __call__(self) -> list[ProjectWithChatsRead]:
        async with self.uow as uow:
            projects = await uow.project.list_all()
        self.logger.debug("projects.listed", count=len(projects))
        return [ProjectWithChatsRead.model_validate(project) for project in projects]
