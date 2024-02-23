from abc import abstractmethod
from datetime import datetime
from uuid import UUID

from domain.core.bus.event.domain_event import DomainEvent
from domain.core.domain_entity import DomainEntity


class AggregateRoot(DomainEntity):
    @abstractmethod
    def __init__(self, id: UUID, created_at: datetime):
        super().__init__(id, created_at)
        self.__events = []

    def pull_events(self) -> [DomainEvent]:
        return self.__events

    def add_event(self, event: DomainEvent) -> None:
        self.__events.append(event)
