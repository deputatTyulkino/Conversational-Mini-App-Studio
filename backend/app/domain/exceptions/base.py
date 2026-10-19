from typing import Any


class DomainError(ValueError):
    """Корень всех доменных ошибок. Наследуется от ValueError."""

    default_message: str = "Domain error"
    code: str = "domain_error"

    def __init__(self, message: str | None = None, **details: Any) -> None:
        self.message = message or self.default_message
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class DomainValidationError(DomainError):
    """Данные не проходят доменные правила (формат, длина, пустота)."""

    default_message = "Validation failed"
    code = "validation_error"


class NotFoundError(DomainError):
    """Сущность не найдена."""

    default_message = "Entity not found"
    code = "not_found"


class AlreadyExistsError(DomainError):
    """Сущность с такими уникальными данными уже существует."""

    default_message = "Entity already exists"
    code = "already_exists"


class ConflictError(DomainError):
    """Операция конфликтует с текущим состоянием (архивирован, уже в проекте и т.п.)."""

    default_message = "Operation conflicts with current state"
    code = "conflict"


class AccessDeniedError(DomainError):
    """У пользователя нет прав на операцию с сущностью."""

    default_message = "Access denied"
    code = "access_denied"


class BusinessRuleViolationError(DomainError):
    """Нарушено бизнес-правило (лимиты, квоты, допустимость операции)."""

    default_message = "Business rule violated"
    code = "business_rule_violation"
