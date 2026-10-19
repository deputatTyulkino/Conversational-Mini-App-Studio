from uuid import UUID

from .base import (
    AccessDeniedError,
    BusinessRuleViolationError,
    ConflictError,
    DomainValidationError,
    NotFoundError,
)


class MessageNotFoundError(NotFoundError):
    code = "message_not_found"

    def __init__(self, message_id: UUID | int | str | None = None) -> None:
        super().__init__(
            f"Message {message_id} not found"
            if message_id is not None
            else "Message not found",
            message_id=message_id,
        )


class MessageContentEmptyError(DomainValidationError):
    code = "message_content_empty"
    default_message = "Message content must not be empty"


class MessageContentTooLongError(DomainValidationError):
    code = "message_content_too_long"

    def __init__(self, max_length: int) -> None:
        super().__init__(
            f"Message content must not exceed {max_length} characters",
            max_length=max_length,
        )


class MessageInvalidRoleError(DomainValidationError):
    code = "message_invalid_role"

    def __init__(self, role: str) -> None:
        super().__init__(f"Invalid message role: {role}", role=role)


class MessageAccessDeniedError(AccessDeniedError):
    code = "message_access_denied"
    default_message = "You have no access to this message"


class MessageNotEditableError(BusinessRuleViolationError):
    """Например, редактировать можно только свои сообщения с ролью user."""

    code = "message_not_editable"
    default_message = "This message cannot be edited"


class MessageNotDeletableError(BusinessRuleViolationError):
    code = "message_not_deletable"
    default_message = "This message cannot be deleted"


class MessageAlreadyDeletedError(ConflictError):
    code = "message_already_deleted"
    default_message = "Message is already deleted"


class MessageChatMismatchError(ConflictError):
    """Сообщение не принадлежит указанному чату."""

    code = "message_chat_mismatch"
    default_message = "Message does not belong to this chat"
