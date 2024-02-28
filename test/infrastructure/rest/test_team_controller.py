from unittest.mock import MagicMock

import pytest

from app import create_app
from src.application.add_team.add_team_command import AddTeamCommand
from src.domain.core.applicaton_error import ApplicationError

add_team_mock = MagicMock()


@pytest.fixture
def client():
    app = create_app()
    app.container.add_team.override(add_team_mock)
    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as client:
            yield client


def test_should_return_400_when_name_field_is_missing(client):
    result = client.post('/teams', json={})

    assert result.status_code == 400
    assert result.json == {
        'message': "Field 'name' is a required property"
    }


def test_should_return_422_when_there_is_application_error(client):
    add_team_mock.execute.side_effect = ApplicationError("error")
    result = client.post('/teams', json={"name": "F.C. Barcelona"})

    assert result.status_code == 422
    assert result.json == {'message': "error"}
    expected_command = AddTeamCommand(name="F.C. Barcelona")
    add_team_mock.execute.assert_called_once()
    assert isinstance(add_team_mock.execute.call_args.args[0], AddTeamCommand)
    assert add_team_mock.execute.call_args.args[0].name == expected_command.name


def test_should_return_500_when_there_is_a_server_error(client):
    add_team_mock.execute.side_effect = Exception("error")
    result = client.post('/teams', json={"name": "F.C. Barcelona"})

    assert result.status_code == 500
    assert result.json == {'message': "Internal server error"}
    expected_command = AddTeamCommand(name="F.C. Barcelona")
    add_team_mock.execute.assert_called_once()
    assert isinstance(add_team_mock.execute.call_args.args[0], AddTeamCommand)
    assert add_team_mock.execute.call_args.args[0].name == expected_command.name


def test_should_return_201_when_team_created(client):
    result = client.post('/teams', json={"name": "F.C. Barcelona"})

    assert result.status_code == 201
    expected_command = AddTeamCommand(name="F.C. Barcelona")
    add_team_mock.execute.assert_called_once()
    assert isinstance(add_team_mock.execute.call_args.args[0], AddTeamCommand)
    assert add_team_mock.execute.call_args.args[0].name == expected_command.name
