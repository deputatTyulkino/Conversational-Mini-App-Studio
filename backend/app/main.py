from contextlib import asynccontextmanager

from app.config.logging import configure_logging
from app.config.settings import get_settings
from app.infrastructure.db.config import engine, session_factory
from app.presentation.api.error_handlers import register_error_handlers
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.session_factory = session_factory
    setting = get_settings()
    configure_logging(setting)
    yield
    await engine.dispose()


app = FastAPI(title="Conversational-Mini-App-Studio", version="1.0", lifespan=lifespan)
register_error_handlers(app)


@app.get("/health")
async def health():
    return {"status": "ok"}
