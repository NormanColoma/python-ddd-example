from src.application.application_response import ApplicationResponse
from src.application.application_service import ApplicationService
from src.application.sign_player.sign_player_command import SignPlayerCommand
from src.domain.core.bus.event.event_bus import EventBus
from src.domain.team.team import Team
from src.domain.team.team_not_found_error import TeamNotFoundError
from src.domain.team.team_repository import TeamRepository


class SignPlayer(ApplicationService[SignPlayerCommand, ApplicationResponse]):
    def __init__(self, team_repository: TeamRepository, event_bus: EventBus):
        self.team_repository = team_repository
        self.bus = event_bus

    def execute(self, command: SignPlayerCommand) -> None:
        team: Team = self.team_repository.find(command.team_id)

        if team is None:
            raise TeamNotFoundError("Team not found")

        team.sign_player(command.player_name)

        self.team_repository.save(team)
        self.bus.publish(team.pull_events())
