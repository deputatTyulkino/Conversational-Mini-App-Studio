from uuid import UUID

from app.application.schemas.entities.message import MessageCreate, SendMessageResponse
from app.application.schemas.tool_router.tool_router_schema import RouterInput
from app.application.services.messages.assistant_reply import build_assistant_reply
from app.application.services.messages.base_message_services import BaseMessageService
from app.application.services.tool_router.tool_router_service import ToolRouterService
from app.domain.entities.message import MessageRole
from app.domain.exceptions.attachment import AttachmentNotAvailableError
from app.domain.exceptions.chat import ChatNotFoundError
from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger


class CreateMessageService(BaseMessageService):
    def __init__(
        self, uow: IUnitOfWork, logger: ILogger, tool_router: ToolRouterService
    ):
        super().__init__(uow, logger)
        self.tool_router = tool_router

    async def __call__(
        self, chat_id: UUID, message_data: MessageCreate
    ) -> SendMessageResponse:
        async with self.uow as uow:
            chat = await uow.chat.get(chat_id)
            if chat is None:
                raise ChatNotFoundError(chat_id)
            message = chat.add_message(
                role=MessageRole.USER, content=message_data.content
            )
            await uow.message.add(message)
            attached = await uow.attachment.attach_to_message(
                chat_id, message.id, message_data.attachment_ids
            )
            missing = set(message_data.attachment_ids) - {at.id for at in attached}
            if missing:
                raise AttachmentNotAvailableError(missing)
            for attachment in attached:
                attachment.attach_to_message(chat_id, message.id)
            message.replace_attachments(attached)
            assistant_message, decision = build_assistant_reply(
                chat,
                self.tool_router,
                RouterInput(
                    chat_id=chat_id,
                    project_id=chat.project_id,
                    text=message_data.content,
                    attachments=[at.to_value_object() for at in attached],
                ),
                self.logger,
            )
            await uow.message.add(assistant_message)
            await uow.chat.update(chat)
            await uow.commit()
        self.logger.info(
            "message.created",
            chat_id=str(chat_id),
            message_id=str(message.id),
            attachments=len(attached),
            route_status=decision.status.value,
            route_app_id=decision.app_id,
        )
        return SendMessageResponse.build(
            client_message_id=message_data.client_message_id,
            user_message=message,
            assistant_message=assistant_message,
        )
