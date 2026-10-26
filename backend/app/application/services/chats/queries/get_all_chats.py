from app.application.schemas.chat import ChatRead
from app.application.services.chats.base_chat_service import BaseChatService


class GetPinedChatsService(BaseChatService):
    async def __call__(self) -> list[ChatRead]:
        async with self.uow as uow:
            pined_chat = await uow.chat.list_pinned()
        return [ChatRead(**chat.as_dict()) for chat in pined_chat]


class GetStanaloneChatsService(BaseChatService):
    async def __call__(self) -> list[ChatRead]:
        async with self.uow as uow:
            standalone_chats = await uow.chat.list_standalone()
        return [ChatRead(**chat.as_dict()) for chat in standalone_chats]
