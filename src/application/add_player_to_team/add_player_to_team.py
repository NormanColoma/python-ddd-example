from src.application.add_player_to_team.add_player_to_team_command import AddPlayerToTeamCommand
from src.application.application_service import ApplicationService
from src.domain.core.bus.event.event_bus import EventBus
from src.domain.team.team import Team
from src.domain.team.team_not_found_error import TeamNotFoundError
from src.domain.team.team_repository import TeamRepository


class AddPlayerToTeam(ApplicationService):
    def __init__(self, team_repository: TeamRepository, event_bus: EventBus):
        self.team_repository = team_repository
        self.bus = event_bus

    def execute(self, command: AddPlayerToTeamCommand) -> None:
        command_fields = command.getFields()
        team: Team = self.team_repository.find(command_fields['team_id'])

        if team is None:
            raise TeamNotFoundError('Team not found')

        team.add_player(command_fields['player_name'])

        self.team_repository.save(team)
        self.bus.publish(team.pull_events())
