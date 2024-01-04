import uuid

from application.add_team.add_team_command import AddTeamCommand
from domain.team.team import Team
from domain.team.team_repository import TeamRepository


class AddTeam:
    def __init__(self, team_repository: TeamRepository):
        self.team_repository = team_repository

    def add(self, command: AddTeamCommand) -> None:
        command_fields = command.getFields()
        team: Team = Team.create(name=command_fields['name'], id=uuid.uuid4())
        self.team_repository.save(team)
