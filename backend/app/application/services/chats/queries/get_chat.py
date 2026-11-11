from uuid import UUID

from app.application.schemas.entities.chat import ChatRead
from app.application.services.chats.base_chat_service import BaseChatService
from app.domain.exceptions.chat import ChatNotFoundError


class GetChatService(BaseChatService):
    async def __call__(self, chat_id: UUID) -> ChatRead:
        async with self.uow as uow:
            chat = await uow.chat.get(chat_id)
        if chat is None:
            self.logger.info("chat.not_found", action="get", chat_id=str(chat_id))
            raise ChatNotFoundError(chat_id)
        self.logger.debug("chat.fetched", chat_id=str(chat_id))
        return ChatRead.model_validate(chat)
