from app.application.schemas.entities.chat import ChatRead
from app.application.services.chats.base_chat_service import BaseChatService


class GetPinnedChatsService(BaseChatService):
    async def __call__(self) -> list[ChatRead]:
        async with self.uow as uow:
            chats = await uow.chat.list_pinned()
        self.logger.debug("chats.pinned_listed", count=len(chats))
        return [ChatRead.model_validate(chat) for chat in chats]


class GetStandaloneChatsService(BaseChatService):
    async def __call__(self) -> list[ChatRead]:
        async with self.uow as uow:
            chats = await uow.chat.list_standalone()
        self.logger.debug("chats.standalone_listed", count=len(chats))
        return [ChatRead.model_validate(chat) for chat in chats]
