import uuid
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.application.add_team.add_team import AddTeam
from src.application.add_team.add_team_command import AddTeamCommand
from src.domain.team.team import Team

id: UUID = uuid.UUID('cdd8f937-52a2-4291-baf1-51520c41a2ab')
created_at_str = "2022-12-14T12:28:17.893609Z"
createdAt = datetime.fromisoformat(created_at_str)
name: str = 'team'

repository = MagicMock()
event_bus = MagicMock()


@pytest.fixture
def app_service():
    add_team = AddTeam(repository, event_bus)
    repository.reset_mock()
    event_bus.reset_mock()
    yield add_team


def test_should_add_team_correctly(mocker, app_service):
    mocker.patch('uuid.uuid4', return_value=id)
    team_domain = mocker.patch('src.domain.team.team')

    expected_team: Team = Team(name, id, createdAt)
    team_domain.create.return_value = expected_team

    command: AddTeamCommand = AddTeamCommand(name)
    app_service.execute(command)

    repository.save.assert_called_once_with(expected_team)
