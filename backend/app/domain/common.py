from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from app.domain.exceptions.base import DomainValidationError

if TYPE_CHECKING:
    from app.domain.events.events import DomainEvent


def utcnow() -> datetime:
    return datetime.now(UTC)


def require_text(value: str, field_name: str, max_length: int) -> str:
    value = value.strip()
    if not value:
        raise DomainValidationError(f"{field_name} не может быть пустым")
    if len(value) > max_length:
        raise DomainValidationError(f"{field_name} длиннее {max_length} символов")
    return value


@dataclass(eq=False)
class AggregateRoot:
    """Корень агрегата: копит доменные события до коммита."""

    _events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

    def _record(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        events, self._events = self._events, []
        return events
