from uuid import UUID

from app.application.schemas.entities.chat import ChatIdRead
from app.application.services.chats.base_chat_service import BaseChatService
from app.domain.exceptions.chat import ChatNotFoundError


class DeleteChatService(BaseChatService):
    async def __call__(self, chat_id: UUID) -> ChatIdRead:
        async with self.uow as uow:
            chat = await uow.chat.get(chat_id)
            if chat is None:
                self.logger.info(
                    "chat.not_found", action="delete", chat_id=str(chat_id)
                )
                raise ChatNotFoundError(chat_id)
            chat.mark_deleted()
            await uow.chat.delete(chat_id)
            await uow.commit()
        self.logger.info(
            "chat.deleted",
            chat_id=str(chat_id),
            project_id=str(chat.project_id) if chat.project_id else None,
        )
        return ChatIdRead(chat_id=chat_id)
