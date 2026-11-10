from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.events.events import DomainEvent


def utcnow() -> datetime:
    return datetime.now(UTC)


@dataclass(eq=False)
class AggregateRoot:
    """Корень агрегата: копит доменные события до коммита."""

    _events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

    def _record(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        events, self._events = self._events, []
        return events
