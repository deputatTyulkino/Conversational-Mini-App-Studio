from uuid import UUID

from app.application.schemas.entities.chat import ChatCreate
from app.application.services.chats.base_chat_service import BaseChatService
from app.domain.entities.chat import ChatDomain
from app.domain.exceptions.project import ProjectNotFoundError


class CreateChatService(BaseChatService):
    async def __call__(self, chat_data: ChatCreate) -> dict[str, UUID]:
        async with self.uow as uow:
            if chat_data.project_id is not None:
                project = await uow.project.get(chat_data.project_id)
                if project is None:
                    raise ProjectNotFoundError(chat_data.project_id)
                chat = (
                    project.create_chat(chat_data.title)
                    if chat_data.title is not None
                    else project.create_chat()
                )
                _ = await uow.project.update(project)
            else:
                chat = ChatDomain.create(**chat_data.model_dump())
            await uow.chat.add(chat)
            await uow.commit()
        return {"chat_id": chat.id}
