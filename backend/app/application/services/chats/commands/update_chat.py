from uuid import UUID

from app.application.schemas.chat import ChatUpdate
from app.application.services.chats.base_chat_service import BaseChatService
from app.domain.entities.chat import ChatDomain
from app.domain.exceptions.chat import ChatNotFoundError


class UpdateChatService(BaseChatService):
    async def __call__(self, chat_id: UUID, chat_data: ChatUpdate) -> dict[str, UUID]:
        async with self.uow as uow:
            exists_chat = await uow.chat.exists(chat_id)
            if not exists_chat:
                raise ChatNotFoundError(chat_id)
            updated_chat_id = await uow.chat.update(
                ChatDomain(id=chat_id, **chat_data.model_dump())
            )
        await uow.commit()
        return {"chat_id": updated_chat_id}
