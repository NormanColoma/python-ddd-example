import uuid
from unittest.mock import MagicMock

import pytest

from app import create_app
from src.application.create_team.create_team_command import CreateTeamCommand
from src.application.get_team.get_team_command import GetTeamCommand
from src.application.sign_player.sign_player_command import SignPlayerCommand
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


class TestCreateTeamEndpoint:
    @pytest.fixture
    def create_team_mock(self):
        create_team_mock = MagicMock()
        yield create_team_mock

    @pytest.fixture
    def client(self, app, create_team_mock):
        app.container.create_team.override(create_team_mock)

        with app.app_context():
            with app.test_client() as client:
                yield client

    def test_should_return_400_when_name_field_is_missing(self, client):
        result = client.post('/teams', json={})

        assert result.status_code == 400
        assert result.json == {
            'message': "Field 'name' is a required property"
        }

    def test_should_return_422_when_there_is_application_error(self, client, create_team_mock):
        create_team_mock.execute.side_effect = ApplicationError("error")
        result = client.post('/teams', json={"name": "F.C. Barcelona"})

        assert result.status_code == 422
        assert result.json == {'message': "error"}
        expected_command = CreateTeamCommand(name="F.C. Barcelona")
        create_team_mock.execute.assert_called_once()
        assert isinstance(create_team_mock.execute.call_args.args[0], CreateTeamCommand)
        assert create_team_mock.execute.call_args.args[0].name == expected_command.name

    def test_should_return_500_when_there_is_a_server_error(self, client, create_team_mock):
        create_team_mock.execute.side_effect = Exception("error")
        result = client.post('/teams', json={"name": "F.C. Barcelona"})

        assert result.status_code == 500
        assert result.json == {'message': "Internal server error"}
        expected_command = CreateTeamCommand(name="F.C. Barcelona")
        create_team_mock.execute.assert_called_once()
        assert isinstance(create_team_mock.execute.call_args.args[0], CreateTeamCommand)
        assert create_team_mock.execute.call_args.args[0].name == expected_command.name

    def test_should_return_201_when_team_created(self, client, create_team_mock):
        result = client.post('/teams', json={"name": "F.C. Barcelona"})

        assert result.status_code == 201
        expected_command = CreateTeamCommand(name="F.C. Barcelona")
        create_team_mock.execute.assert_called_once()
        assert isinstance(create_team_mock.execute.call_args.args[0], CreateTeamCommand)
        assert create_team_mock.execute.call_args.args[0].name == expected_command.name


class TestSignPlayerEndpoint:
    @pytest.fixture
    def sign_player_mock(self):
        sign_player_mock = MagicMock()
        yield sign_player_mock

    @pytest.fixture
    def client(self, app, sign_player_mock):
        app.container.sign_player.override(sign_player_mock)

        with app.app_context():
            with app.test_client() as client:
                yield client

    def test_should_return_404_when_team_is_not_found(self, client, sign_player_mock):
        sign_player_mock.execute.side_effect = TeamNotFoundError("error")
        result = client.post('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2/players', json={"name": player_name})

        assert result.status_code == 404
        assert result.json == {'message': "error"}
        expected_command = SignPlayerCommand(player_name, team_id)
        sign_player_mock.execute.assert_called_once()
        assert isinstance(sign_player_mock.execute.call_args.args[0], SignPlayerCommand)
        assert sign_player_mock.execute.call_args.args[0].player_name == expected_command.player_name
        assert sign_player_mock.execute.call_args.args[0].team_id == expected_command.team_id

    def test_should_return_422_when_there_is_application_error(self, client, sign_player_mock):
        sign_player_mock.execute.side_effect = ApplicationError("error")
        result = client.post('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2/players', json={"name": player_name})

        assert result.status_code == 422
        assert result.json == {'message': "error"}
        expected_command = SignPlayerCommand(player_name, team_id)
        sign_player_mock.execute.assert_called_once()
        assert isinstance(sign_player_mock.execute.call_args.args[0], SignPlayerCommand)
        assert sign_player_mock.execute.call_args.args[0].player_name == expected_command.player_name
        assert sign_player_mock.execute.call_args.args[0].team_id == expected_command.team_id

    def test_should_return_500_when_there_is_internal_error(self, client, sign_player_mock):
        sign_player_mock.execute.side_effect = Exception("error")
        result = client.post('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2/players', json={"name": player_name})

        assert result.status_code == 500
        assert result.json == {'message': "Internal server error"}
        expected_command = SignPlayerCommand(player_name, team_id)
        sign_player_mock.execute.assert_called_once()
        assert isinstance(sign_player_mock.execute.call_args.args[0], SignPlayerCommand)
        assert sign_player_mock.execute.call_args.args[0].player_name == expected_command.player_name
        assert sign_player_mock.execute.call_args.args[0].team_id == expected_command.team_id

    def test_should_return_201_when_player_signed(self, client, sign_player_mock):
        result = client.post('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2/players', json={"name": player_name})

        assert result.status_code == 201
        expected_command = SignPlayerCommand(player_name, team_id)
        sign_player_mock.execute.assert_called_once()
        assert isinstance(sign_player_mock.execute.call_args.args[0], SignPlayerCommand)
        assert sign_player_mock.execute.call_args.args[0].player_name == expected_command.player_name
        assert sign_player_mock.execute.call_args.args[0].team_id == expected_command.team_id


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
