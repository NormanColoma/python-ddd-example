import uuid
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.application.add_team.add_team import AddTeam
from src.application.add_team.add_team_command import AddTeamCommand

id: UUID = uuid.UUID('cdd8f937-52a2-4291-baf1-51520c41a2ab')
created_at_str = "2022-12-14T12:28:17.893609Z"
createdAt = datetime.fromisoformat(created_at_str)
name: str = 'team'

repository = MagicMock()
event_bus = MagicMock()


@pytest.fixture
def app_service():
    add_team = AddTeam(repository, event_bus)
    yield add_team
    repository.reset_mock()
    event_bus.reset_mock()


def test_should_add_team_correctly(mocker, app_service):
    mocker.patch('uuid.uuid4', return_value=id)
    team_mock = MagicMock()
    team_mock.pull_events.return_value = []
    create_mock = mocker.patch('src.domain.team.team.Team.create', return_value=team_mock)

    command: AddTeamCommand = AddTeamCommand(name)
    app_service.execute(command)

    create_mock.assert_called_once_with(name=name, id=id)
    team_mock.pull_events.assert_called_once()
    event_bus.publish.assert_called_once_with([])
