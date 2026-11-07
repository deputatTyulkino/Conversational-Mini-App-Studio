from uuid import UUID

from app.application.schemas.entities.message import (
    MessageCreate,
    MessageRead,
    SendMessageResponse,
)
from app.application.schemas.tool_router.tool_router_schema import (
    RouteDecision,
    RouteFallbackReason,
    RouteStatus,
)
from app.application.services.messages.base_message_services import BaseMessageService
from app.application.services.tool_router.tool_router_service import ToolRouterService
from app.domain.entities.message import MessageRole
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
                content="Откройте и работайте в подходящем приложении",
                payload=decision.model_dump(),
            )
            await uow.message.add(assistant_message)
            await uow.chat.update(chat)
            await uow.commit()
        return SendMessageResponse(
            client_message_id=message.id,
            user_message=MessageRead(**message.as_dict()),
            assistant_message=MessageRead(**assistant_message.as_dict()),
        )
