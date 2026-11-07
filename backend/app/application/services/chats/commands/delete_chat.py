from uuid import UUID

from app.application.services.chats.base_chat_service import BaseChatService
from app.domain.exceptions.chat import ChatNotFoundError


class DeleteChatService(BaseChatService):
    async def __call__(self, chat_id: UUID) -> dict[str, UUID]:
        async with self.uow as uow:
            chat = await uow.chat.get(chat_id)
            if chat is None:
                raise ChatNotFoundError(chat_id)
            chat.mark_deleted()
            deleted_chat_id = await uow.chat.delete(chat_id)
            await uow.commit()
        return {"chat_id": deleted_chat_id}
