from .base import (
    AlreadyExistsHTTPException,
    BusinessRuleHTTPException,
    ConflictHTTPException,
    ForbiddenHTTPException,
    NotFoundHTTPException,
    ValidationHTTPException,
)


class ChatNotFoundHTTPException(NotFoundHTTPException):
    code = "chat_not_found"
    default_message = "Chat not found"


class ChatAlreadyExistsHTTPException(AlreadyExistsHTTPException):
    code = "chat_already_exists"
    default_message = "Chat already exists"


class ChatTitleEmptyHTTPException(ValidationHTTPException):
    code = "chat_title_empty"
    default_message = "Chat title must not be empty"


class ChatTitleTooLongHTTPException(ValidationHTTPException):
    code = "chat_title_too_long"
    default_message = "Chat title is too long"


class ChatAccessDeniedHTTPException(ForbiddenHTTPException):
    code = "chat_access_denied"
    default_message = "You have no access to this chat"


class ChatArchivedHTTPException(ConflictHTTPException):
    code = "chat_archived"
    default_message = "Chat is archived"


class ChatAlreadyArchivedHTTPException(ConflictHTTPException):
    code = "chat_already_archived"
    default_message = "Chat is already archived"


class ChatNotArchivedHTTPException(ConflictHTTPException):
    code = "chat_not_archived"
    default_message = "Chat is not archived"


class ChatLimitExceededHTTPException(BusinessRuleHTTPException):
    code = "chat_limit_exceeded"
    default_message = "Chat limit exceeded"
