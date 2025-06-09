from abc import abstractmethod
from datetime import datetime
from typing import Generic, List
from uuid import UUID

from src.domain.core.bus.event.domain_event import DomainEvent
from src.domain.core.domain_entity import DomainEntity
from src.domain.types import E


class AggregateRoot(DomainEntity, Generic[E]):
    @abstractmethod
    def __init__(self, id: UUID, created_at: datetime):
        super().__init__(id, created_at)
        self.__events = []

    def pull_events(
        self,
    ) -> List[DomainEvent[E]]:
        events = self.__events
        self.__events = []
        return events

    def add_event(self, event: DomainEvent[E]) -> None:
        if isinstance(event, DomainEvent):
            self.__events.append(event)
