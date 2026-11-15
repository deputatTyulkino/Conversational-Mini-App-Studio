from app.application.schemas.entities.message import RoutePayload
from app.application.schemas.tool_router.tool_router_schema import (
    RouteDecision,
    RouteFallbackReason,
    RouterInput,
    RouteStatus,
)
from app.application.services.tool_router.tool_router_service import ToolRouterService
from app.domain.entities.chat import ChatDomain
from app.domain.entities.message import MessageDomain, MessageRole
from app.domain.logging.i_logger import ILogger

ASSISTANT_REPLIES = {
    RouteStatus.MATCHED: "Откройте и работайте в подходящем приложении",
    RouteStatus.AMBIGUOUS: "Уточните, с каким приложением хотите работать",
    RouteStatus.NONE: "Не удалось подобрать приложение",
}


def build_assistant_reply(
    chat: ChatDomain,
    tool_router: ToolRouterService,
    route_input: RouterInput,
    logger: ILogger,
) -> tuple[MessageDomain, RouteDecision]:
    try:
        decision = tool_router(route_input)
    except Exception:
        logger.exception("tool_router.failed", chat_id=str(chat.id))
        decision = RouteDecision(
            status=RouteStatus.NONE,
            confidence=0.0,
            fallback_reason=RouteFallbackReason.ROUTER_ERROR,
        )
    message = chat.add_message(
        role=MessageRole.ASSISTANT,
        content=ASSISTANT_REPLIES[decision.status],
        payload=RoutePayload(decision=decision).model_dump(mode="json"),
    )
    return message, decision
