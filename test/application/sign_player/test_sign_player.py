import uuid
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.application.sign_player.sign_player import SignPlayer
from src.application.sign_player.sign_player_command import SignPlayerCommand
from src.domain.team.team_not_found_error import TeamNotFoundError

team_id: UUID = uuid.UUID("cdd8f937-52a2-4291-baf1-51520c41a2ab")
created_at_str = "2022-12-14T12:28:17.893609Z"
createdAt = datetime.fromisoformat(created_at_str)
name: str = "Messi"

repository = MagicMock()
event_bus = MagicMock()


@pytest.fixture
def app_service():
    app_service = SignPlayer(repository, event_bus)
    yield app_service
    repository.reset_mock()
    event_bus.reset_mock()


def test_should_raise_exception_when_given_team_not_found(mocker, app_service):
    team_domain_mock = mocker.patch("src.domain.team.team")
    repository.find.return_value = None

    command = SignPlayerCommand(name, team_id)

    with pytest.raises(TeamNotFoundError) as e:
        app_service.execute(command)
    assert e.value.message == "Team not found"

    repository.find.assert_called_once_with(team_id)
    repository.save.assert_not_called()
    team_domain_mock.sign_player.assert_not_called()
    team_domain_mock.pull_events.assert_not_called()
    event_bus.publish.assert_not_called()


def test_should_sign_player_correctly(mocker, app_service):
    team_domain_mock = mocker.patch("src.domain.team.team")
    repository.find.return_value = team_domain_mock

    command = SignPlayerCommand(name, team_id)
    app_service.execute(command)

    repository.find.assert_called_once_with(team_id)
    repository.save.assert_called_once_with(team_domain_mock)
    team_domain_mock.sign_player.assert_called_once_with(name)
    team_domain_mock.pull_events.assert_called_once()
    event_bus.publish.assert_called_once()
