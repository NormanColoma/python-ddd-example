import uuid

from application.add_team.add_team_command import AddTeamCommand
from domain.core.bus.event.event_bus import EventBus
from domain.team.team import Team
from domain.team.team_repository import TeamRepository


class AddTeam:
    def __init__(self, team_repository: TeamRepository, event_bus: EventBus):
        self.team_repository = team_repository
        self.bus = event_bus

    def add(self, command: AddTeamCommand) -> None:
        command_fields = command.getFields()
        team: Team = Team.create(name=command_fields['name'], id=uuid.uuid4())
        self.team_repository.save(team)

        self.bus.publish(team.pull_events())