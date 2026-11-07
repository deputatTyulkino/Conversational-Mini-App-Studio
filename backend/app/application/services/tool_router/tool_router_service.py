from app.application.schemas.tool_router.tool_router_schema import RouteDecision


class ToolRouterService:
    def __call__(self) -> RouteDecision: ...
