from uuid import UUID

from app.application.schemas.entities.message import MessageListParams, MessagePage
from app.application.services.messages.base_message_services import BaseMessageService
from app.domain.exceptions.chat import ChatNotFoundError


class GetAllMessagesService(BaseMessageService):
    async def __call__(
        self, chat_id: UUID, data_params: MessageListParams
    ) -> MessagePage:
        async with self.uow as uow:
            exists_chat = await uow.chat.exists(chat_id)
            if not exists_chat:
                raise ChatNotFoundError(chat_id)
            messages = await uow.message.list_by_chat(
                chat_id,
                data_params.limit,
                data_params.before_created_at,
                data_params.before_id,
            )
        return MessagePage.build(messages, data_params.limit)
