from typing import Any

from fastapi import HTTPException, status


class ApiHTTPException(HTTPException):
    """Корень всех HTTP-ошибок presentation-слоя."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "api_error"
    default_message: str = "Request failed"

    def __init__(
        self,
        message: str | None = None,
        *,
        code: str | None = None,
        details: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.message = message or self.default_message
        self.code = code or self.code
        self.details = details or {}
        super().__init__(
            status_code=self.status_code,
            detail=self.message,
            headers=headers,
        )


class ValidationHTTPException(ApiHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = "validation_error"
    default_message = "Validation failed"


class NotFoundHTTPException(ApiHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"
    default_message = "Entity not found"


class AlreadyExistsHTTPException(ApiHTTPException):
    status_code = status.HTTP_409_CONFLICT
    code = "already_exists"
    default_message = "Entity already exists"


class ConflictHTTPException(ApiHTTPException):
    status_code = status.HTTP_409_CONFLICT
    code = "conflict"
    default_message = "Operation conflicts with current state"


class ForbiddenHTTPException(ApiHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    code = "access_denied"
    default_message = "Access denied"


class BusinessRuleHTTPException(ApiHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "business_rule_violation"
    default_message = "Business rule violated"
