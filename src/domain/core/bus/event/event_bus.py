from abc import ABC, abstractmethod

from src.domain.core.bus.event.domain_event import DomainEvent


class EventBus(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def publish(self, events: [DomainEvent]) -> None:
        raise NotImplementedError("Method publish must be implemented")
