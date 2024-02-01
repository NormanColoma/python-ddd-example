from application.get_team.get_team_command import GetTeamCommand
from application.get_team.get_team_response import GetTeamResponse
from domain.team.team import Team
from domain.team.team_not_found_error import TeamNotFoundError
from domain.team.team_repository import TeamRepository


class GetTeam:
    def __init__(self, team_repository: TeamRepository):
        self.team_repository = team_repository

    def get(self, command: GetTeamCommand) -> GetTeamResponse:
        command_fields = command.getFields()
        team: Team = self.team_repository.find(command_fields['id'])

        if team is None:
            raise TeamNotFoundError('Team not found')

        return GetTeamResponse(team)
