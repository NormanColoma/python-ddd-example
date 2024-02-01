from domain.core.bus.event.domain_event import DomainEvent
from domain.core.domain_entity import DomainEntity


class AggregateRoot(DomainEntity):
    def __init__(self, id, created_at):
        super().__init__(id, created_at)
        self.__events = []

    def pull_events(self):
        return self.__events

    def add_event(self, event: DomainEvent):
        self.__events.append(event)
