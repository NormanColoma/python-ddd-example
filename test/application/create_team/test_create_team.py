import uuid
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.application.create_team.create_team import CreateTeam
from src.application.create_team.create_team_command import CreateTeamCommand

id: UUID = uuid.UUID('cdd8f937-52a2-4291-baf1-51520c41a2ab')
created_at_str = "2022-12-14T12:28:17.893609Z"
createdAt = datetime.fromisoformat(created_at_str)
name: str = 'team'

repository = MagicMock()
event_bus = MagicMock()


@pytest.fixture
def app_service():
    add_team = CreateTeam(repository, event_bus)
    yield add_team
    repository.reset_mock()
    event_bus.reset_mock()


def test_should_add_team_correctly(mocker, app_service):
    mocker.patch('uuid.uuid4', return_value=id)
    team_mock = MagicMock()
    team_mock.pull_events.return_value = []
    create_mock = mocker.patch('src.domain.team.team.Team.create', return_value=team_mock)

    command: CreateTeamCommand = CreateTeamCommand(name)
    app_service.execute(command)

    create_mock.assert_called_once_with(name=name, id=id)
    team_mock.pull_events.assert_called_once()
    event_bus.publish.assert_called_once_with([])
