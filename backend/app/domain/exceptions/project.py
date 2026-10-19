from uuid import UUID

from .base import (
    AccessDeniedError,
    AlreadyExistsError,
    BusinessRuleViolationError,
    ConflictError,
    DomainValidationError,
    NotFoundError,
)


class ProjectNotFoundError(NotFoundError):
    code = "project_not_found"

    def __init__(self, project_id: UUID | int | str | None = None) -> None:
        super().__init__(
            f"Project {project_id} not found"
            if project_id is not None
            else "Project not found",
            project_id=project_id,
        )


class ProjectAlreadyExistsError(AlreadyExistsError):
    code = "project_already_exists"

    def __init__(self, name: str | None = None) -> None:
        super().__init__(
            f"Project '{name}' already exists" if name else "Project already exists",
            name=name,
        )


class ProjectNameEmptyError(DomainValidationError):
    code = "project_name_empty"
    default_message = "Project name must not be empty"


class ProjectNameTooLongError(DomainValidationError):
    code = "project_name_too_long"

    def __init__(self, max_length: int) -> None:
        super().__init__(
            f"Project name must not exceed {max_length} characters",
            max_length=max_length,
        )


class ProjectAccessDeniedError(AccessDeniedError):
    code = "project_access_denied"
    default_message = "You have no access to this project"


class ProjectArchivedError(ConflictError):
    code = "project_archived"
    default_message = "Project is archived"


class ProjectAlreadyArchivedError(ConflictError):
    code = "project_already_archived"
    default_message = "Project is already archived"


class ProjectNotArchivedError(ConflictError):
    code = "project_not_archived"
    default_message = "Project is not archived"


class ProjectLimitExceededError(BusinessRuleViolationError):
    code = "project_limit_exceeded"

    def __init__(self, limit: int) -> None:
        super().__init__(f"Project limit exceeded (max {limit})", limit=limit)


class ChatAlreadyInProjectError(ConflictError):
    code = "chat_already_in_project"
    default_message = "Chat is already in this project"


class ChatNotInProjectError(ConflictError):
    code = "chat_not_in_project"
    default_message = "Chat is not in this project"
