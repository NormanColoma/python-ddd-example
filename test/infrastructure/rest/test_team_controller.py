import uuid
from unittest.mock import MagicMock

import pytest

from app import create_app
from src.application.add_player_to_team.add_player_to_team_command import AddPlayerToTeamCommand
from src.application.add_team.add_team_command import AddTeamCommand
from src.application.get_team.get_team_command import GetTeamCommand
from src.domain.core.applicaton_error import ApplicationError
from src.domain.team.team_not_found_error import TeamNotFoundError

team_name = "F.C. Barcelona"
player_name = "Messi"
team_id = uuid.UUID("e154e156-6d6f-402f-b571-d83fc7d605f2")


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True

    yield app


class TestAddTeamEndpoint:
    @pytest.fixture
    def add_team_mock(self):
        add_team_mock = MagicMock()
        yield add_team_mock

    @pytest.fixture
    def client(self, app, add_team_mock):
        app.container.add_team.override(add_team_mock)

        with app.app_context():
            with app.test_client() as client:
                yield client

    def test_should_return_400_when_name_field_is_missing(self, client):
        result = client.post('/teams', json={})

        assert result.status_code == 400
        assert result.json == {
            'message': "Field 'name' is a required property"
        }

    def test_should_return_422_when_there_is_application_error(self, client, add_team_mock):
        add_team_mock.execute.side_effect = ApplicationError("error")
        result = client.post('/teams', json={"name": "F.C. Barcelona"})

        assert result.status_code == 422
        assert result.json == {'message': "error"}
        expected_command = AddTeamCommand(name="F.C. Barcelona")
        add_team_mock.execute.assert_called_once()
        assert isinstance(add_team_mock.execute.call_args.args[0], AddTeamCommand)
        assert add_team_mock.execute.call_args.args[0].name == expected_command.name

    def test_should_return_500_when_there_is_a_server_error(self, client, add_team_mock):
        add_team_mock.execute.side_effect = Exception("error")
        result = client.post('/teams', json={"name": "F.C. Barcelona"})

        assert result.status_code == 500
        assert result.json == {'message': "Internal server error"}
        expected_command = AddTeamCommand(name="F.C. Barcelona")
        add_team_mock.execute.assert_called_once()
        assert isinstance(add_team_mock.execute.call_args.args[0], AddTeamCommand)
        assert add_team_mock.execute.call_args.args[0].name == expected_command.name

    def test_should_return_201_when_team_created(self, client, add_team_mock):
        result = client.post('/teams', json={"name": "F.C. Barcelona"})

        assert result.status_code == 201
        expected_command = AddTeamCommand(name="F.C. Barcelona")
        add_team_mock.execute.assert_called_once()
        assert isinstance(add_team_mock.execute.call_args.args[0], AddTeamCommand)
        assert add_team_mock.execute.call_args.args[0].name == expected_command.name


class TestAddPlayerToTeamEndpoint:
    @pytest.fixture
    def add_player_to_team_mock(self):
        add_player_to_team_mock = MagicMock()
        yield add_player_to_team_mock

    @pytest.fixture
    def client(self, app, add_player_to_team_mock):
        app.container.add_player_to_team.override(add_player_to_team_mock)

        with app.app_context():
            with app.test_client() as client:
                yield client

    def test_should_return_404_when_team_is_not_found(self, client, add_player_to_team_mock):
        add_player_to_team_mock.execute.side_effect = TeamNotFoundError("error")
        result = client.post('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2/players', json={"name": player_name})

        assert result.status_code == 404
        assert result.json == {'message': "error"}
        expected_command = AddPlayerToTeamCommand(player_name, team_id)
        add_player_to_team_mock.execute.assert_called_once()
        assert isinstance(add_player_to_team_mock.execute.call_args.args[0], AddPlayerToTeamCommand)
        assert add_player_to_team_mock.execute.call_args.args[0].player_name == expected_command.player_name
        assert add_player_to_team_mock.execute.call_args.args[0].team_id == expected_command.team_id

    def test_should_return_422_when_there_is_application_error(self, client, add_player_to_team_mock):
        add_player_to_team_mock.execute.side_effect = ApplicationError("error")
        result = client.post('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2/players', json={"name": player_name})

        assert result.status_code == 422
        assert result.json == {'message': "error"}
        expected_command = AddPlayerToTeamCommand(player_name, team_id)
        add_player_to_team_mock.execute.assert_called_once()
        assert isinstance(add_player_to_team_mock.execute.call_args.args[0], AddPlayerToTeamCommand)
        assert add_player_to_team_mock.execute.call_args.args[0].player_name == expected_command.player_name
        assert add_player_to_team_mock.execute.call_args.args[0].team_id == expected_command.team_id

    def test_should_return_500_when_there_is_internal_error(self, client, add_player_to_team_mock):
        add_player_to_team_mock.execute.side_effect = Exception("error")
        result = client.post('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2/players', json={"name": player_name})

        assert result.status_code == 500
        assert result.json == {'message': "Internal server error"}
        expected_command = AddPlayerToTeamCommand(player_name, team_id)
        add_player_to_team_mock.execute.assert_called_once()
        assert isinstance(add_player_to_team_mock.execute.call_args.args[0], AddPlayerToTeamCommand)
        assert add_player_to_team_mock.execute.call_args.args[0].player_name == expected_command.player_name
        assert add_player_to_team_mock.execute.call_args.args[0].team_id == expected_command.team_id

    def test_should_return_201_when_player_added_to_team(self, client, add_player_to_team_mock):
        result = client.post('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2/players', json={"name": player_name})

        assert result.status_code == 201
        expected_command = AddPlayerToTeamCommand(player_name, team_id)
        add_player_to_team_mock.execute.assert_called_once()
        assert isinstance(add_player_to_team_mock.execute.call_args.args[0], AddPlayerToTeamCommand)
        assert add_player_to_team_mock.execute.call_args.args[0].player_name == expected_command.player_name
        assert add_player_to_team_mock.execute.call_args.args[0].team_id == expected_command.team_id


class TestGetTeamGetEndpoint:
    @pytest.fixture
    def get_team_mock(self):
        get_team_mock = MagicMock()
        yield get_team_mock

    @pytest.fixture
    def client(self, app, get_team_mock):
        app.container.get_team.override(get_team_mock)

        with app.app_context():
            with app.test_client() as client:
                yield client

    def test_should_return_404_when_team_is_not_found(self, client, get_team_mock):
        get_team_mock.execute.side_effect = TeamNotFoundError("error")
        result = client.get('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2')

        assert result.status_code == 404
        assert result.json == {'message': "error"}
        expected_command = GetTeamCommand(id=team_id)
        get_team_mock.execute.assert_called_once()
        assert isinstance(get_team_mock.execute.call_args.args[0], GetTeamCommand)
        assert get_team_mock.execute.call_args.args[0].id == expected_command.id

    def test_should_return_422_when_there_is_application_error(self, client, get_team_mock):
        get_team_mock.execute.side_effect = ApplicationError("error")
        result = client.get('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2')

        assert result.status_code == 422
        assert result.json == {'message': "error"}
        expected_command = GetTeamCommand(id=team_id)
        get_team_mock.execute.assert_called_once()
        assert isinstance(get_team_mock.execute.call_args.args[0], GetTeamCommand)
        assert get_team_mock.execute.call_args.args[0].id == expected_command.id

    def test_should_return_500_when_there_is_internal_error(self, client, get_team_mock):
        get_team_mock.execute.side_effect = Exception("error")
        result = client.get('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2')

        assert result.status_code == 500
        assert result.json == {'message': "Internal server error"}
        expected_command = GetTeamCommand(id=team_id)
        get_team_mock.execute.assert_called_once()
        assert isinstance(get_team_mock.execute.call_args.args[0], GetTeamCommand)
        assert get_team_mock.execute.call_args.args[0].id == expected_command.id

    def test_should_return_200_when_retrieving_given_team(self, client, get_team_mock):
        get_team_response_mock = MagicMock()
        get_team_mock.execute.return_value = get_team_response_mock
        get_team_response_mock.to_json.return_value = {
            'id': str(team_id),
            'name': team_name,
            'created_at': '2023/12/12 00:10:05',
            'players': [
                {
                    'name': player_name,
                    'created_at': '2023/12/12 01:10:05'
                }
            ]
        }
        result = client.get('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2')

        assert result.status_code == 200
        assert result.json == {
            'id': str(team_id),
            'name': team_name,
            'created_at': '2023/12/12 00:10:05',
            'players': [
                {
                    'name': player_name,
                    'created_at': '2023/12/12 01:10:05'
                }
            ]
        }
        expected_command = GetTeamCommand(id=team_id)
        get_team_mock.execute.assert_called_once()
        assert isinstance(get_team_mock.execute.call_args.args[0], GetTeamCommand)
        assert get_team_mock.execute.call_args.args[0].id == expected_command.id
        get_team_response_mock.to_json.assert_called_once()
