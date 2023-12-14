from application.application_command import ApplicationCommand
from domain.team.team import Team
from domain.team.team_repository import TeamRepository


class AddTeam:
    def __init__(self, team_repository: TeamRepository):
        self.team_repository = team_repository

    def save(self, command: ApplicationCommand) -> None:
        command_fields = command.getFields()
        team: Team = Team.create(**command_fields)
        print('Saving team')
        self.team_repository.save(team)
