from collections.abc import Iterator
from contextlib import contextmanager

from app.domain.exceptions import base as d
from app.domain.exceptions import chat as dc
from app.domain.exceptions import message as dm
from app.domain.exceptions import project as dp

from . import chat as c
from . import message as m
from . import project as p
from .base import (
    AlreadyExistsHTTPException,
    ApiHTTPException,
    BusinessRuleHTTPException,
    ConflictHTTPException,
    ForbiddenHTTPException,
    NotFoundHTTPException,
    ValidationHTTPException,
)

_DOMAIN_TO_HTTP: dict[type[d.DomainError], type[ApiHTTPException]] = {
    # категории
    d.DomainValidationError: ValidationHTTPException,
    d.NotFoundError: NotFoundHTTPException,
    d.AlreadyExistsError: AlreadyExistsHTTPException,
    d.ConflictError: ConflictHTTPException,
    d.AccessDeniedError: ForbiddenHTTPException,
    d.BusinessRuleViolationError: BusinessRuleHTTPException,
    # chat
    dc.ChatNotFoundError: c.ChatNotFoundHTTPException,
    dc.ChatAlreadyExistsError: c.ChatAlreadyExistsHTTPException,
    dc.ChatTitleEmptyError: c.ChatTitleEmptyHTTPException,
    dc.ChatTitleTooLongError: c.ChatTitleTooLongHTTPException,
    dc.ChatAccessDeniedError: c.ChatAccessDeniedHTTPException,
    dc.ChatArchivedError: c.ChatArchivedHTTPException,
    dc.ChatAlreadyArchivedError: c.ChatAlreadyArchivedHTTPException,
    dc.ChatNotArchivedError: c.ChatNotArchivedHTTPException,
    dc.ChatLimitExceededError: c.ChatLimitExceededHTTPException,
    # message
    dm.MessageNotFoundError: m.MessageNotFoundHTTPException,
    dm.MessageContentEmptyError: m.MessageContentEmptyHTTPException,
    dm.MessageContentTooLongError: m.MessageContentTooLongHTTPException,
    dm.MessageInvalidRoleError: m.MessageInvalidRoleHTTPException,
    dm.MessageAccessDeniedError: m.MessageAccessDeniedHTTPException,
    dm.MessageNotEditableError: m.MessageNotEditableHTTPException,
    dm.MessageNotDeletableError: m.MessageNotDeletableHTTPException,
    dm.MessageAlreadyDeletedError: m.MessageAlreadyDeletedHTTPException,
    dm.MessageChatMismatchError: m.MessageChatMismatchHTTPException,
    # project
    dp.ProjectNotFoundError: p.ProjectNotFoundHTTPException,
    dp.ProjectAlreadyExistsError: p.ProjectAlreadyExistsHTTPException,
    dp.ProjectNameEmptyError: p.ProjectNameEmptyHTTPException,
    dp.ProjectNameTooLongError: p.ProjectNameTooLongHTTPException,
    dp.ProjectAccessDeniedError: p.ProjectAccessDeniedHTTPException,
    dp.ProjectArchivedError: p.ProjectArchivedHTTPException,
    dp.ProjectAlreadyArchivedError: p.ProjectAlreadyArchivedHTTPException,
    dp.ProjectNotArchivedError: p.ProjectNotArchivedHTTPException,
    dp.ProjectLimitExceededError: p.ProjectLimitExceededHTTPException,
    dp.ChatAlreadyInProjectError: p.ChatAlreadyInProjectHTTPException,
    dp.ChatNotInProjectError: p.ChatNotInProjectHTTPException,
}


def to_http_error(exc: d.DomainError) -> ApiHTTPException:
    """Превращает доменную ошибку в HTTP-ошибку, сохраняя message/code/details."""
    for cls in type(exc).__mro__:
        http_cls = _DOMAIN_TO_HTTP.get(cls)
        if http_cls is not None:
            return http_cls(exc.message, code=exc.code, details=exc.details)
    return BusinessRuleHTTPException(exc.message, code=exc.code, details=exc.details)


@contextmanager
def translate_domain_errors() -> Iterator[None]:
    """Контекстный менеджер: DomainError -> ApiHTTPException."""
    try:
        yield
    except d.DomainError as exc:
        raise to_http_error(exc) from exc
