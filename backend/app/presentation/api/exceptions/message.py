from .base import (
    BusinessRuleHTTPException,
    ConflictHTTPException,
    ForbiddenHTTPException,
    NotFoundHTTPException,
    ValidationHTTPException,
)


class MessageNotFoundHTTPException(NotFoundHTTPException):
    code = "message_not_found"
    default_message = "Message not found"


class MessageContentEmptyHTTPException(ValidationHTTPException):
    code = "message_content_empty"
    default_message = "Message content must not be empty"


class MessageContentTooLongHTTPException(ValidationHTTPException):
    code = "message_content_too_long"
    default_message = "Message content is too long"


class MessageInvalidRoleHTTPException(ValidationHTTPException):
    code = "message_invalid_role"
    default_message = "Invalid message role"


class MessageAccessDeniedHTTPException(ForbiddenHTTPException):
    code = "message_access_denied"
    default_message = "You have no access to this message"


class MessageNotEditableHTTPException(BusinessRuleHTTPException):
    code = "message_not_editable"
    default_message = "This message cannot be edited"


class MessageNotDeletableHTTPException(BusinessRuleHTTPException):
    code = "message_not_deletable"
    default_message = "This message cannot be deleted"


class MessageAlreadyDeletedHTTPException(ConflictHTTPException):
    code = "message_already_deleted"
    default_message = "Message is already deleted"


class MessageChatMismatchHTTPException(ConflictHTTPException):
    code = "message_chat_mismatch"
    default_message = "Message does not belong to this chat"
