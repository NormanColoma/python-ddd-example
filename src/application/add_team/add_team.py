import uuid

from src.application.add_team.add_team_command import AddTeamCommand
from src.application.application_service import ApplicationService
from src.domain.core.bus.event.event_bus import EventBus
from src.domain.team.team import Team
from src.domain.team.team_repository import TeamRepository


class AddTeam(ApplicationService):
    def __init__(self, team_repository: TeamRepository, event_bus: EventBus):
        self.team_repository = team_repository
        self.bus = event_bus

    def execute(self, command: AddTeamCommand) -> None:
        team: Team = Team.create(name=command.name, id=uuid.uuid4())
        self.team_repository.save(team)

        self.bus.publish(team.pull_events())
