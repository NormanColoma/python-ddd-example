from src.application.application_service import ApplicationService
from src.application.get_team.get_team_command import GetTeamCommand
from src.application.get_team.get_team_response import GetTeamResponse
from src.domain.team.team import Team
from src.domain.team.team_not_found_error import TeamNotFoundError
from src.domain.team.team_repository import TeamRepository


class GetTeam(ApplicationService):
    def __init__(self, team_repository: TeamRepository):
        self.team_repository = team_repository

    def execute(self, command: GetTeamCommand) -> GetTeamResponse:
        team: Team = self.team_repository.find(command.id)

        if team is None:
            raise TeamNotFoundError("Team not found")

        return GetTeamResponse(team)
