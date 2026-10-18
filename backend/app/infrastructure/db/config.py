from app.config.settings import get_settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

settings = get_settings()

engine = create_async_engine(
    url=settings.database_dsn, echo=settings.database_echo, pool_pre_ping=True
)

session_factory = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass
