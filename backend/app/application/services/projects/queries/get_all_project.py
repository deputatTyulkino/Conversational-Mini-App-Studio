from app.application.schemas.project import ProjectRead
from app.application.services.projects.base_project_services import BaseProjectServcies


class GetAllProjectService(BaseProjectServcies):
    async def __call__(self) -> list[ProjectRead]:
        async with self.uow as uow:
            projects = await uow.project.list_all()
        return [ProjectRead(**project.as_dict()) for project in projects]
