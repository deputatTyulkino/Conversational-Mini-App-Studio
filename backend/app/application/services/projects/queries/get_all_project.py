import asyncio

from app.application.schemas.entities.project import ProjectWithChatsRead
from app.application.services.projects.base_project_services import BaseProjectServcies
from app.domain.entities.chat import ChatDomain


class GetAllProjectService(BaseProjectServcies):
    async def __call__(self) -> list[ProjectWithChatsRead]:
        async with self.uow as uow:
            projects = await uow.project.list_all()
            chats_coro: list[asyncio.Task[list[ChatDomain]]] = []
            for project in projects:
                chats_coro.append(
                    asyncio.create_task(
                        uow.chat.list_by_project(project.id, limit=10, aside=True)
                    )
                )
            chats: list[list[ChatDomain]] = []
            for coro in chats_coro:
                coro_res = coro.result()
                chats.append(coro_res)
        return [
            ProjectWithChatsRead.build(project, chats)
            for project, chats in zip(projects, chats)
        ]
