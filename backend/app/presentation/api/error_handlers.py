import logging
from http import HTTPStatus
from typing import Any

from app.presentation.api.exceptions.base import ApiHTTPException
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

_LOCATIONS = {"body", "query", "path", "header", "cookie"}

_FRIENDLY_MESSAGES = {
    "missing": "Field is required",
    "json_invalid": "Request body is not valid JSON",
    "string_type": "Value must be a string",
    "int_type": "Value must be an integer",
    "int_parsing": "Value must be a valid integer",
    "bool_parsing": "Value must be a valid boolean",
    "uuid_parsing": "Value must be a valid UUID",
    "string_too_short": "Value is too short",
    "string_too_long": "Value is too long",
    "extra_forbidden": "Unexpected field",
}


def _error_response(
    status_code: int,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        headers=headers,
        content=jsonable_encoder(
            {"error": {"code": code, "message": message, "details": details or {}}}
        ),
    )


def _split_loc(loc: tuple[Any, ...]) -> tuple[str | None, str | None]:
    """('body', 'items', 0, 'name') -> ('body', 'items[0].name')"""
    location = str(loc[0]) if loc and loc[0] in _LOCATIONS else None
    parts = loc[1:] if location else loc

    field = ""
    for part in parts:
        if isinstance(part, int):
            field += f"[{part}]"
        else:
            field += f".{part}" if field else str(part)
    return location, field or None


def _clean_message(error: dict[str, Any]) -> str:
    err_type = error.get("type", "")
    if err_type in _FRIENDLY_MESSAGES:
        return _FRIENDLY_MESSAGES[err_type]

    message = str(error.get("msg", "Invalid value")).removeprefix("Value error, ")
    return message[:1].upper() + message[1:]


def _status_to_code(status_code: int) -> str:
    try:
        return HTTPStatus(status_code).phrase.lower().replace(" ", "_")
    except ValueError:
        return "http_error"


async def validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    if not isinstance(exc, RequestValidationError):
        return JSONResponse(exc)
    validation_exc = exc
    errors = []
    for error in validation_exc.errors():
        location, field = _split_loc(tuple(error.get("loc", ())))
        if error.get("type") == "json_invalid":
            field = None
        item = {
            "location": location,
            "field": field,
            "message": _clean_message(error),
            "type": error.get("type"),
        }
        errors.append({k: v for k, v in item.items() if v is not None})

    count = len(errors)
    return _error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        code="validation_error",
        message=f"Request validation failed ({count} error{'s' if count != 1 else ''})",
        details={"errors": errors},
    )


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Единый формат и для наших ApiHTTPException, и для стандартных (404 роута, 405 и т.д.)."""
    if isinstance(exc, HTTPException):
        if isinstance(exc, ApiHTTPException):
            code, message, details = exc.code, exc.message, exc.details
        else:
            code = _status_to_code(exc.status_code)
            if isinstance(exc.detail, str):
                message, details = exc.detail, {}
            else:
                message, details = "Request failed", {"detail": exc.detail}

        return _error_response(
            exc.status_code,
            code,
            message,
            details,
            headers=getattr(exc, "headers", None),
        )
    return JSONResponse(exc)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return _error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="internal_server_error",
        message="Internal server error",
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
