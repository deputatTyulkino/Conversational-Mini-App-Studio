from uuid import UUID

from app.domain.entities.chat import ChatDomain
from app.domain.entities.project import ProjectDomain
from app.domain.interfaces.entities.project import IProjectRepo
from app.domain.logging.i_logger import ILogger
from app.infrastructure.db.models.chats import ChatORM
from app.infrastructure.db.models.projects import ProjectORM
from sqlalchemy import delete, exists, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload


class ProjectRepo(IProjectRepo):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self.session = session
        self.logger = logger

    @staticmethod
    def _chat_to_domain(chat: ChatORM) -> ChatDomain:
        return ChatDomain(
            id=chat.id,
            title=chat.title,
            project_id=chat.project_id,
            is_pinned=chat.is_pinned,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
        )

    @staticmethod
    def _to_domain_model(
        project: ProjectORM, chats: list[ChatDomain] | None = None
    ) -> ProjectDomain:
        return ProjectDomain(
            id=project.id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
            updated_at=project.updated_at,
            chats=chats or [],
        )

    @staticmethod
    def _to_orm_model(project: ProjectDomain) -> ProjectORM:
        return ProjectORM(
            id=project.id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    async def add(self, project: ProjectDomain) -> None:
        self.session.add(self._to_orm_model(project))
        await self.session.flush()
        self.logger.debug("project_repo.add", project_id=str(project.id))

    async def get(self, project_id: UUID) -> ProjectDomain | None:
        query = select(ProjectORM).filter(ProjectORM.id == project_id)
        project = (await self.session.execute(query)).scalar_one_or_none()
        if project is None:
            return None
        return self._to_domain_model(project)

    async def get_with_chats(self, project_id: UUID) -> ProjectDomain | None:
        query = (
            select(ProjectORM)
            .filter(ProjectORM.id == project_id)
            .options(selectinload(ProjectORM.chats))
        )
        project = (await self.session.execute(query)).scalar_one_or_none()
        if project is None:
            return None
        return self._to_domain_model(
            project, [self._chat_to_domain(chat) for chat in project.chats]
        )

    async def update(self, project: ProjectDomain) -> None:
        stmt = (
            update(ProjectORM)
            .filter(ProjectORM.id == project.id)
            .values(
                name=project.name,
                description=project.description,
                updated_at=project.updated_at,
            )
            .returning(ProjectORM.id)
        )
        updated_id = (await self.session.execute(stmt)).scalar_one_or_none()
        if updated_id is None:
            self.logger.warning(
                "project_repo.update_no_rows", project_id=str(project.id)
            )
            return
        self.logger.debug("project_repo.update", project_id=str(project.id))

    async def delete(self, project_id: UUID) -> None:
        stmt = (
            delete(ProjectORM)
            .filter(ProjectORM.id == project_id)
            .returning(ProjectORM.id)
        )
        deleted_id = (await self.session.execute(stmt)).scalar_one_or_none()
        if deleted_id is None:
            self.logger.warning(
                "project_repo.delete_no_rows", project_id=str(project_id)
            )
            return
        self.logger.debug("project_repo.delete", project_id=str(project_id))

    async def exists(self, project_id: UUID) -> bool:
        query = select(exists(ProjectORM).where(ProjectORM.id == project_id))
        return (await self.session.execute(query)).scalar_one()

    async def list_all(
        self, limit: int = 8, chats_per_project: int = 5
    ) -> list[ProjectDomain]:
        projects_stmt = (
            select(ProjectORM)
            .order_by(ProjectORM.created_at.desc(), ProjectORM.id)
            .limit(limit)
        )
        projects = (await self.session.scalars(projects_stmt)).all()
        if not projects:
            self.logger.debug("project_repo.list_all", projects=0, chats=0)
            return []
        projects_ids = [p.id for p in projects]
        rn = (
            func.row_number()
            .over(
                partition_by=ChatORM.project_id,
                order_by=[ChatORM.created_at.desc(), ChatORM.id],
            )
            .label("rn")
        )
        ranked = (
            select(ChatORM, rn).filter(ChatORM.project_id.in_(projects_ids)).subquery()
        )
        chat_alias = aliased(ChatORM, ranked)
        chats_stmt = (
            select(chat_alias)
            .filter(ranked.c.rn <= chats_per_project)
            .order_by(ranked.c.rn, chat_alias.id)
        )
        chats = (await self.session.scalars(chats_stmt)).all()
        grouped: dict[UUID, list[ChatDomain]] = {pid: [] for pid in projects_ids}
        for chat in chats:
            if chat.project_id is None:
                continue
            grouped[chat.project_id].append(self._chat_to_domain(chat))
        self.logger.debug(
            "project_repo.list_all", projects=len(projects), chats=len(chats)
        )
        return [self._to_domain_model(p, grouped[p.id]) for p in projects]
