from uuid import UUID

from app.application.schemas.entities.message import (
    MessageRead,
    MessageUpdate,
    SendMessageResponse,
)
from app.application.schemas.tool_router.tool_router_schema import (
    RouteDecision,
    RouteFallbackReason,
    RouteStatus,
)
from app.application.services.messages.base_message_services import BaseMessageService
from app.application.services.tool_router.tool_router_service import ToolRouterService
from app.domain.entities.message import MessageDomain, MessageRole
from app.domain.exceptions.chat import ChatNotFoundError
from app.domain.exceptions.message import MessageNotFoundError
from app.domain.interfaces.uow.uow_interface import IUnitOfWork
from app.domain.logging.i_logger import ILogger


class UpdateMessageService(BaseMessageService):
    def __init__(
        self, uow: IUnitOfWork, logger: ILogger, tool_router: ToolRouterService
    ):
        super().__init__(uow, logger)
        self.tool_router = tool_router

    async def __call__(
        self, chat_id: UUID, message_id: UUID, message_data: MessageUpdate
    ) -> SendMessageResponse:
        async with self.uow as uow:
            chat = await uow.chat.get(chat_id)
            if chat is None:
                raise ChatNotFoundError(chat_id)
            exists_message = await uow.message.exists(message_id)
            if not exists_message:
                raise MessageNotFoundError(message_id)
            updated_message = MessageDomain.update(
                chat_id=chat_id,
                id=message_id,
                role=MessageRole.USER,
                content=message_data.content,
            )
            updated_message_id = await uow.message.update(updated_message)
            try:
                decision = self.tool_router()  # вызываем tool router
            except ValueError:
                decision = RouteDecision(
                    status=RouteStatus.NONE,
                    confidence=0.0,
                    fallback_reason=RouteFallbackReason.ROUTER_ERROR,
                )
                assistant_message = chat.add_message(
                    role=MessageRole.ASSISTANT,
                    content="Не удалось подобрать приложение",
                    payload=decision.model_dump(),
                )
            else:
                assistant_message = chat.add_message(
                    role=MessageRole.ASSISTANT,
                    content="Откройте и работайте в подходящем приложении",
                    payload=decision.model_dump(),
                )
            await uow.message.add(assistant_message)
            await uow.commit()
        return SendMessageResponse(
            client_message_id=updated_message_id,
            user_message=MessageRead(**updated_message.as_dict()),
            assistant_message=MessageRead(**assistant_message.as_dict()),
        )
