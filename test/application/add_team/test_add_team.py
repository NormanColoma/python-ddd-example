import uuid
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID
from application.add_team.add_team import AddTeam
from application.add_team.add_team_command import AddTeamCommand
from domain.team.team import Team
from domain.team.team_repository import TeamRepository

id: UUID = uuid.UUID('cdd8f937-52a2-4291-baf1-51520c41a2ab')
created_at_str = "2022-12-14T12:28:17.893609Z"
createdAt = datetime.fromisoformat(created_at_str)
name: str = 'team'


def test_should_add_team_correctly(mocker):
    mocker.patch('uuid.uuid4', return_value=id)
    repository: TeamRepository = mocker.patch('domain.team.team_repository')
    team_domain = mocker.patch('domain.team.team')

    add_team: AddTeam = AddTeam(repository)

    repository.save = MagicMock()
    expected_team: Team = Team(name, id, createdAt)
    team_domain.create.return_value = expected_team

    command: AddTeamCommand = AddTeamCommand(name)
    add_team.add(command)

    repository.save.assert_called_once_with(expected_team)
