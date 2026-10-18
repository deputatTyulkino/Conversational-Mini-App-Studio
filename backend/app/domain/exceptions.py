class DomainError(Exception):
    """Базовая ошибка домена."""


class DomainValidationError(DomainError):
    """Нарушен инвариант сущности."""
