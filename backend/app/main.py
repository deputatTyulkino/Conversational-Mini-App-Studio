from contextlib import asynccontextmanager

from app.config.logging import configure_logging
from app.config.settings import get_settings
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    setting = get_settings()
    configure_logging(setting)
    yield
    ...


app = FastAPI(title="Conversational-Mini-App-Studio", version="1.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}
