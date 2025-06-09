from src.domain.core.bus.event.domain_event import DomainEvent
from src.domain.team.team import Team


class TeamModifiedEvent(DomainEvent[Team]):
    def __init__(self, entity: Team, name="team-modified"):
        super().__init__(entity, name)
