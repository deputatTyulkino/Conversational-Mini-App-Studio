from uuid import UUID

from app.application.schemas.entities.message import MessageListParams, MessagePage
from app.application.services.messages.base_message_services import BaseMessageService


class GetAllMessagesService(BaseMessageService):
    async def __call__(
        self, chat_id: UUID, data_params: MessageListParams
    ) -> MessagePage:
        async with self.uow as uow:
            messages = await uow.message.list_by_chat(
                chat_id, **data_params.model_dump()
            )
        return MessagePage.build(messages, data_params.limit)
