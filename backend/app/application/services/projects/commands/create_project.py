from uuid import UUID

from app.application.schemas.project import ProjectCreate
from app.application.services.projects.base_project_services import BaseProjectServcies
from app.domain.entities.project import ProjectDomain


class CreateProjectService(BaseProjectServcies):
    async def __call__(self, project_data: ProjectCreate) -> dict[str, UUID]:
        async with self.uow as uow:
            domain_project = ProjectDomain.create(**project_data.model_dump())
            await uow.project.add(domain_project)
        return {"project_id": domain_project.id}
