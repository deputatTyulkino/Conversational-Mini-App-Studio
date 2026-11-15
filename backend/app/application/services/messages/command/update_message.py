from uuid import UUID

from app.application.schemas.entities.message import (
    MessageUpdate,
    SendMessageResponse,
)
from app.application.schemas.tool_router.tool_router_schema import RouterInput
from app.application.services.messages.assistant_reply import build_assistant_reply
from app.application.services.messages.base_message_services import BaseMessageService
from app.application.services.tool_router.tool_router_service import ToolRouterService
from app.domain.exceptions.attachment import AttachmentNotAvailableError
from app.domain.exceptions.chat import ChatNotFoundError
from app.domain.exceptions.message import MessageChatMismatchError, MessageNotFoundError
from app.domain.interfaces.storage.file_storage import IFileStorage
from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger


class UpdateMessageService(BaseMessageService):
    def __init__(
        self,
        uow: IUnitOfWork,
        logger: ILogger,
        tool_router: ToolRouterService,
        file_storage: IFileStorage,
    ):
        super().__init__(uow, logger)
        self.tool_router = tool_router
        self.file_storage = file_storage

    async def __call__(
        self, chat_id: UUID, message_id: UUID, message_data: MessageUpdate
    ) -> SendMessageResponse:
        requested = message_data.attachment_ids
        requested_set = set(requested)
        async with self.uow as uow:
            chat = await uow.chat.get(chat_id)
            if chat is None:
                raise ChatNotFoundError(chat_id)
            message = await uow.message.get(message_id)
            if message is None:
                raise MessageNotFoundError(message_id)
            if message.chat_id != chat_id:
                raise MessageChatMismatchError()
            message.change_content(message_data.content)
            await uow.message.update(message)
            current = {at.id: at for at in message.attachments}
            new_ids = [item for item in requested if item not in current]
            removed_ids = [item for item in current if item not in requested_set]
            attached = await uow.attachment.attach_to_message(
                chat_id, message_id, new_ids
            )
            missing = set(new_ids) - {at.id for at in attached}
            if missing:
                raise AttachmentNotAvailableError(missing)
            for attachment in attached:
                attachment.attach_to_message(message_id)
            removed_paths = await uow.attachment.delete_from_message(
                message_id, removed_ids
            )
            by_id = {**current, **{at.id: at for at in attached}}
            final_attachments = [by_id[item] for item in requested]
            message.replace_attachments(final_attachments)
            assistant_message, decision = build_assistant_reply(
                chat,
                self.tool_router,
                RouterInput(
                    chat_id=chat_id,
                    project_id=chat.project_id,
                    text=message.content,
                    attachments=[at.to_value_object() for at in final_attachments],
                ),
                self.logger,
            )
            await uow.message.add(assistant_message)
            await uow.chat.update(chat)
            await uow.commit()
        await self.file_storage.delete_many(removed_paths)
        self.logger.info(
            "message.updated",
            chat_id=str(chat_id),
            message_id=str(message_id),
            attached=len(attached),
            removed=len(removed_paths),
            route_status=decision.status.value,
        )
        return SendMessageResponse.build(
            client_message_id=None,
            user_message=message,
            assistant_message=assistant_message,
        )
