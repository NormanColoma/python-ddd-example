from application.add_team.add_team_command import AddTeamCommand
from application.application_command import ApplicationCommand
from domain.team.team import Team
from domain.team.team_repository import TeamRepository


class AddTeam:
    def __init__(self, team_repository: TeamRepository):
        self.team_repository = team_repository

    def add(self, command: AddTeamCommand) -> None:
        command_fields = command.getFields()
        team: Team = Team.create(**command_fields)
        self.team_repository.save(team)
