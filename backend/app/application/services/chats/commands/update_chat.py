from uuid import UUID

from app.application.schemas.entities.chat import ChatUpdate
from app.application.services.chats.base_chat_service import BaseChatService
from app.domain.exceptions.chat import ChatNotFoundError
from app.domain.exceptions.project import ProjectNotFoundError


class UpdateChatService(BaseChatService):
    async def __call__(self, chat_id: UUID, chat_data: ChatUpdate) -> dict[str, UUID]:
        async with self.uow as uow:
            chat = await uow.chat.get(chat_id)
            if chat is None:
                raise ChatNotFoundError(chat_id)
            if chat_data.title is not None:
                chat.rename(chat_data.title)
            if chat_data.is_pinned is not None:
                if chat_data.is_pinned:
                    chat.pin()
                else:
                    chat.unpin()
            if chat_data.project_id is not None:
                exists_project = await uow.project.exists(chat_data.project_id)
                if not exists_project:
                    raise ProjectNotFoundError(chat_data.project_id)
                chat.move_to_project(chat_data.project_id)
            updated_chat_id = await uow.chat.update(chat)
            await uow.commit()
        return {"chat_id": updated_chat_id}
