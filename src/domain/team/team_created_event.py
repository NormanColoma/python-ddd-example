from src.domain.core.bus.event.domain_event import DomainEvent
from src.domain.core.domain_entity import DomainEntity


class TeamCreatedEvent(DomainEvent):
    def __init__(self, entity: DomainEntity, name="team-created"):
        super().__init__(entity, name)
