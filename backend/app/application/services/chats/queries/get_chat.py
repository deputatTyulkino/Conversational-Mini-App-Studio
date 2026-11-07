from uuid import UUID

from app.application.schemas.entities.chat import ChatRead
from app.application.services.chats.base_chat_service import BaseChatService
from app.domain.exceptions.chat import ChatNotFoundError


class GetChatService(BaseChatService):
    async def __call__(self, chat_id: UUID) -> ChatRead:
        async with self.uow as uow:
            chat = await uow.chat.get(chat_id)
        if chat is None:
            raise ChatNotFoundError(chat_id)
        return ChatRead(**chat.as_dict())
