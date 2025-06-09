from src.domain.core.bus.event.domain_event import DomainEvent
from src.domain.team.team import Team


class TeamCreatedEvent(DomainEvent[Team]):
    def __init__(self, entity: Team, name="team-created"):
        super().__init__(entity, name)
