from uuid import UUID

from app.domain.entities.project import ProjectDomain
from app.domain.interfaces.entities.project import IProject
from app.domain.logging.i_logger import ILogger
from app.infrastructure.db.models.projects import ProjectORM
from sqlalchemy import delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class ProjectRepo(IProject):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self.session = session
        self.logger = logger

    def _to_domain_model(self, project: ProjectORM) -> ProjectDomain:
        return ProjectDomain(
            id=project.id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    def _to_orm_model(self, project: ProjectDomain) -> ProjectORM:
        return ProjectORM(
            id=project.id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    async def add(self, project: ProjectDomain) -> UUID:
        new_project = self._to_orm_model(project)
        self.session.add(new_project)
        await self.session.flush()
        return new_project.id

    async def get(self, project_id: UUID) -> ProjectDomain | None:
        query = select(ProjectORM).filter(ProjectORM.id == project_id)
        project = (await self.session.execute(query)).scalar_one_or_none()
        if project is None:
            return None
        return self._to_domain_model(project)

    async def update(self, project: ProjectDomain) -> UUID:
        stmt = (
            update(ProjectORM)
            .filter(ProjectORM.id == project.id)
            .values(**project.as_dict())
            .returning(ProjectORM.id)
        )
        updated_project_id = (await self.session.execute(stmt)).scalar_one()
        return updated_project_id

    async def delete(self, project_id: UUID) -> UUID:
        stmt = (
            delete(ProjectORM)
            .filter(ProjectORM.id == project_id)
            .returning(ProjectORM.id)
        )
        deleted_project_id = (await self.session.execute(stmt)).scalar_one()
        return deleted_project_id

    async def exists(self, project_id: UUID) -> bool:
        query = select(exists(ProjectORM).where(ProjectORM.id == project_id))
        exists_project = (await self.session.execute(query)).scalar_one()
        return exists_project

    async def list_all(self) -> list[ProjectDomain]:
        query = select(ProjectORM)
        projects = (await self.session.scalars(query)).all()
        return [self._to_domain_model(project) for project in projects]
