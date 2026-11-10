from app.application.schemas.tool_router.tool_router_schema import RouteDecision


class ToolRouterService:
    def __init__(self): ...
    def __call__(self) -> RouteDecision: ...


def build_tool_router() -> ToolRouterService:
    return ToolRouterService()
