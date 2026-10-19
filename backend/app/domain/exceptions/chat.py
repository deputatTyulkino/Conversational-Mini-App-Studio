from uuid import UUID

from .base import (
    AccessDeniedError,
    AlreadyExistsError,
    BusinessRuleViolationError,
    ConflictError,
    DomainValidationError,
    NotFoundError,
)


class ChatNotFoundError(NotFoundError):
    code = "chat_not_found"

    def __init__(self, chat_id: UUID | int | str | None = None) -> None:
        super().__init__(
            f"Chat {chat_id} not found" if chat_id is not None else "Chat not found",
            chat_id=chat_id,
        )


class ChatAlreadyExistsError(AlreadyExistsError):
    code = "chat_already_exists"
    default_message = "Chat already exists"


class ChatTitleEmptyError(DomainValidationError):
    code = "chat_title_empty"
    default_message = "Chat title must not be empty"


class ChatTitleTooLongError(DomainValidationError):
    code = "chat_title_too_long"

    def __init__(self, max_length: int) -> None:
        super().__init__(
            f"Chat title must not exceed {max_length} characters",
            max_length=max_length,
        )


class ChatAccessDeniedError(AccessDeniedError):
    code = "chat_access_denied"
    default_message = "You have no access to this chat"


class ChatArchivedError(ConflictError):
    """Попытка изменить/писать в архивированный чат."""

    code = "chat_archived"
    default_message = "Chat is archived"


class ChatAlreadyArchivedError(ConflictError):
    code = "chat_already_archived"
    default_message = "Chat is already archived"


class ChatNotArchivedError(ConflictError):
    code = "chat_not_archived"
    default_message = "Chat is not archived"


class ChatLimitExceededError(BusinessRuleViolationError):
    code = "chat_limit_exceeded"

    def __init__(self, limit: int) -> None:
        super().__init__(f"Chat limit exceeded (max {limit})", limit=limit)
