from app.application.schemas.entities.project import (
    ProjectCreate,
    ProjectRead,
)
from app.application.services.projects.base_project_services import BaseProjectServices
from app.domain.entities.project import ProjectDomain


class CreateProjectService(BaseProjectServices):
    async def __call__(self, project_data: ProjectCreate) -> ProjectRead:
        async with self.uow as uow:
            project = ProjectDomain.create(**project_data.model_dump())
            await uow.project.add(project)
            await uow.commit()
        self.logger.info("project.created", project_id=str(project.id))
        return ProjectRead.model_validate(project)
