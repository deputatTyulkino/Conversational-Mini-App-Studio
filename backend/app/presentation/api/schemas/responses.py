from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Успешный ответ с одним объектом."""

    data: T
    meta: dict[str, Any] = Field(default_factory=dict)


class PaginationMeta(BaseModel):
    total: int = Field(description="Всего элементов")
    limit: int = Field(description="Размер страницы")
    offset: int = Field(description="Смещение от начала")
    has_more: bool = Field(description="Есть ли следующая страница")


class PaginatedResponse(BaseModel, Generic[T]):
    """Успешный ответ со списком и пагинацией."""

    data: list[T]
    meta: PaginationMeta


class MessageData(BaseModel):
    message: str


class MessageResponse(SuccessResponse[MessageData]):
    """Для действий без полезной нагрузки (архивация, восстановление и т.п.)."""


class ErrorBody(BaseModel):
    code: str = Field(examples=["chat_not_found"])
    message: str = Field(examples=["Chat not found"])
    details: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    error: ErrorBody


class ValidationErrorItem(BaseModel):
    location: str | None = Field(default=None, examples=["body"])
    field: str | None = Field(default=None, examples=["title"])
    message: str = Field(examples=["Field is required"])
    type: str | None = Field(default=None, examples=["missing"])


class ValidationErrorDetails(BaseModel):
    errors: list[ValidationErrorItem]


class ValidationErrorBody(BaseModel):
    code: str = Field(default="validation_error")
    message: str = Field(examples=["Request validation failed (1 error)"])
    details: ValidationErrorDetails


class ValidationErrorResponse(BaseModel):
    error: ValidationErrorBody
