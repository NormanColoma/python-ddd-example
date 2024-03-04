import uuid
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.application.get_team.get_team import GetTeam
from src.application.get_team.get_team_command import GetTeamCommand
from src.application.get_team.get_team_response import GetTeamResponse
from src.domain.team.team_not_found_error import TeamNotFoundError

team_id: UUID = uuid.UUID('cdd8f937-52a2-4291-baf1-51520c41a2ab')
created_at_str = "2022-12-14T12:28:17.893609Z"
createdAt = datetime.fromisoformat(created_at_str)
name: str = 'Messi'

repository = MagicMock()


@pytest.fixture
def app_service():
    app_service = GetTeam(repository)
    yield app_service
    repository.reset_mock()


def test_should_raise_exception_when_given_team_not_found(app_service):
    repository.find.return_value = None

    command = GetTeamCommand(team_id)

    with pytest.raises(TeamNotFoundError) as e:
        app_service.execute(command)
    assert e.value.message == 'Team not found'

    repository.find.assert_called_once_with(team_id)
    repository.save.assert_not_called()


def test_should_add_player_to_team_correctly(mocker, app_service):
    team_domain_mock = mocker.patch('src.domain.team.team')
    mocker.patch('src.application.get_team.get_team_response')
    repository.find.return_value = team_domain_mock

    command = GetTeamCommand(team_id)
    response = app_service.execute(command)

    repository.find.assert_called_once_with(team_id)
    assert isinstance(response, GetTeamResponse)
