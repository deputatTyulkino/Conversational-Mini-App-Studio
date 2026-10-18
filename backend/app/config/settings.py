from functools import lru_cache
from pathlib import Path
from typing import Literal, Self

from pydantic import Field, PostgresDsn, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]

RATE_LIMIT_PATTERN = r"^\d+/(second|minute|hour|day)$"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_ignore_empty=True,
    )

    app_env: Literal["local", "test", "staging", "production"] = "local"
    app_name: str = "Conversational Mini-App Studio"
    app_debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_json: bool = False

    public_base_url: str = "http://localhost:5173"
    frontend_url: str = "http://localhost:5173"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    database_url: PostgresDsn
    database_echo: bool = False
    database_pool_size: int = Field(default=10, ge=1)
    database_max_overflow: int = Field(default=10, ge=0)

    session_secret_key: SecretStr
    auth_session_cookie_name: str = "studio_session"
    auth_session_ttl_seconds: int = Field(default=604_800, gt=0)  # 7 дней
    auth_cookie_secure: bool = False
    auth_cookie_samesite: Literal["lax", "strict", "none"] = "lax"
    auth_cookie_domain: str | None = None

    yandex_client_id: str
    yandex_client_secret: SecretStr

    github_client_id: str
    github_client_secret: SecretStr

    router_confidence_threshold: float = Field(default=0.55, ge=0.0, le=1.0)
    router_ambiguity_margin: float = Field(default=0.10, ge=0.0, le=1.0)
    router_top_k: int = Field(default=3, ge=1)

    ui_schema_max_depth: int = Field(default=12, ge=1)
    ui_schema_max_nodes: int = Field(default=2000, ge=1)
    ui_schema_max_bytes: int = Field(default=524_288, ge=1)

    storage_dir: Path = Path("./storage")
    upload_max_bytes: int = Field(default=10_485_760, ge=1)  # 10 MiB
    upload_allowed_extensions: list[str] = Field(
        default_factory=lambda: ["csv", "json"]
    )

    confirmation_ttl_seconds: int = Field(default=300, gt=0)

    rate_limit_auth: str = Field(default="20/minute", pattern=RATE_LIMIT_PATTERN)
    rate_limit_upload: str = Field(default="10/minute", pattern=RATE_LIMIT_PATTERN)

    @field_validator("cors_origins")
    @classmethod
    def _strip_trailing_slash(cls, v: list[str]) -> list[str]:
        return [origin.rstrip("/") for origin in v]

    @field_validator("public_base_url", "frontend_url")
    @classmethod
    def _strip_url(cls, v: str) -> str:
        return v.rstrip("/")

    @field_validator("upload_allowed_extensions")
    @classmethod
    def _normalize_extensions(cls, v: list[str]) -> list[str]:
        return [ext.lower().lstrip(".") for ext in v]

    @field_validator("storage_dir")
    @classmethod
    def _resolve_storage_dir(cls, v: Path) -> Path:
        return v if v.is_absolute() else (BASE_DIR / v).resolve()

    @model_validator(mode="after")
    def _check_consistency(self) -> Self:
        problems: list[str] = []

        if self.auth_cookie_samesite == "none" and not self.auth_cookie_secure:
            problems.append(
                "AUTH_COOKIE_SAMESITE=none requires AUTH_COOKIE_SECURE=true"
            )

        if self.app_env == "production":
            if self.session_secret_key.get_secret_value().startswith("change-me"):
                problems.append("SESSION_SECRET_KEY must be changed in production")
            if len(self.session_secret_key.get_secret_value()) < 32:
                problems.append("SESSION_SECRET_KEY must be at least 32 characters")
            if not self.auth_cookie_secure:
                problems.append("AUTH_COOKIE_SECURE must be true in production")
            if self.app_debug:
                problems.append("APP_DEBUG must be false in production")

        if problems:
            raise ValueError("; ".join(problems))
        return self

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def database_dsn(self) -> str:
        return str(self.database_url)

    def oauth_callback_url(self, provider: str) -> str:
        return f"{self.public_base_url}/api/v1/auth/{provider}/callback"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
