from .base import (
    AlreadyExistsHTTPException,
    BusinessRuleHTTPException,
    ConflictHTTPException,
    ForbiddenHTTPException,
    NotFoundHTTPException,
    ValidationHTTPException,
)


class ProjectNotFoundHTTPException(NotFoundHTTPException):
    code = "project_not_found"
    default_message = "Project not found"


class ProjectAlreadyExistsHTTPException(AlreadyExistsHTTPException):
    code = "project_already_exists"
    default_message = "Project already exists"


class ProjectNameEmptyHTTPException(ValidationHTTPException):
    code = "project_name_empty"
    default_message = "Project name must not be empty"


class ProjectNameTooLongHTTPException(ValidationHTTPException):
    code = "project_name_too_long"
    default_message = "Project name is too long"


class ProjectAccessDeniedHTTPException(ForbiddenHTTPException):
    code = "project_access_denied"
    default_message = "You have no access to this project"


class ProjectArchivedHTTPException(ConflictHTTPException):
    code = "project_archived"
    default_message = "Project is archived"


class ProjectAlreadyArchivedHTTPException(ConflictHTTPException):
    code = "project_already_archived"
    default_message = "Project is already archived"


class ProjectNotArchivedHTTPException(ConflictHTTPException):
    code = "project_not_archived"
    default_message = "Project is not archived"


class ProjectLimitExceededHTTPException(BusinessRuleHTTPException):
    code = "project_limit_exceeded"
    default_message = "Project limit exceeded"


class ChatAlreadyInProjectHTTPException(ConflictHTTPException):
    code = "chat_already_in_project"
    default_message = "Chat is already in this project"


class ChatNotInProjectHTTPException(ConflictHTTPException):
    code = "chat_not_in_project"
    default_message = "Chat is not in this project"
