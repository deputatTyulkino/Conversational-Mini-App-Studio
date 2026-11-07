from contextlib import asynccontextmanager

from app.config.logging import configure_logging
from app.config.settings import get_settings
from app.infrastructure.db.config import engine, session_factory
from app.presentation.api.error_handlers import register_error_handlers
from app.presentation.api.schemas.responses import ValidationErrorResponse
from app.presentation.routers.chat import router as chats_router
from app.presentation.routers.message import router as messages_router
from app.presentation.routers.project import router as projects_router
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.session_factory = session_factory
    setting = get_settings()
    configure_logging(setting)
    yield
    await engine.dispose()


app = FastAPI(
    title="Conversational-Mini-App-Studio",
    version="1.0",
    lifespan=lifespan,
    responses={422: {"model": ValidationErrorResponse}},
)
register_error_handlers(app)

chats_router.include_router(messages_router)
app.include_router(projects_router)
app.include_router(chats_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
