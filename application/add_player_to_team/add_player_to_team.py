from application.add_player_to_team.add_player_to_team_command import AddPlayerToTeamCommand
from domain.team.team import Team
from domain.team.team_not_found_error import TeamNotFoundError
from domain.team.team_repository import TeamRepository


class AddPlayerToTeam:
    def __init__(self, team_repository: TeamRepository):
        self.team_repository = team_repository

    def add(self, command: AddPlayerToTeamCommand) -> None:
        command_fields = command.getFields()
        team: Team = self.team_repository.find(command_fields['team_id'])

        if team is None:
            raise TeamNotFoundError('Team not found')

        team.add_player(command_fields['player_name'])
        self.team_repository.save(team)
