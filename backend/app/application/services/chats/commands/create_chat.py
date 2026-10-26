from uuid import UUID

from app.application.schemas.chat import ChatCreate
from app.application.services.chats.base_chat_service import BaseChatService
from app.domain.entities.chat import ChatDomain


class CreateChatService(BaseChatService):
    async def __call__(self, chat_data: ChatCreate) -> dict[str, UUID]:
        async with self.uow as uow:
            domain_chat = ChatDomain.create(**chat_data.model_dump())
            await uow.chat.add(domain_chat)
        await uow.commit()
        return {"chat_id": domain_chat.id}
