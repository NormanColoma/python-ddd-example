from domain.core.bus.event.domain_event import DomainEvent
from domain.core.bus.event.event_bus import EventBus


class FakeEventBus(EventBus):
    def publish(self, events: [DomainEvent]) -> None:
        print('publishing domain events...')

    def __init__(self):
        pass
