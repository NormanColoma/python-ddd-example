from application.application_command import ApplicationCommand
from application.get_team.get_team_response import GetTeamResponse
from domain.team.team import Team
from domain.team.team_repository import TeamRepository


class GetTeam:
    def __init__(self, team_repository: TeamRepository):
        self.team_repository = team_repository

    def get(self, command: ApplicationCommand) -> GetTeamResponse:
        command_fields = command.getFields()
        team: Team = self.team_repository.find(command_fields['id'])

        return GetTeamResponse(team)
