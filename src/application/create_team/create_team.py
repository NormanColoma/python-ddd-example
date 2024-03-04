import uuid

from src.application.application_service import ApplicationService
from src.application.create_team.create_team_command import CreateTeamCommand
from src.domain.core.bus.event.event_bus import EventBus
from src.domain.team.team import Team
from src.domain.team.team_repository import TeamRepository


class CreateTeam(ApplicationService):
    def __init__(self, team_repository: TeamRepository, event_bus: EventBus):
        self.team_repository = team_repository
        self.bus = event_bus

    def execute(self, command: CreateTeamCommand) -> None:
        team: Team = Team.create(name=command.name, id=uuid.uuid4())
        self.team_repository.save(team)

        self.bus.publish(team.pull_events())
