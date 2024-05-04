import uuid
from unittest.mock import patch

import pytest

from app import create_app
from src.application.create_team.create_team import CreateTeam
from src.application.get_team.get_team import GetTeam
from src.application.sign_player.sign_player import SignPlayer
from src.container import Container
from src.domain.core.applicaton_error import ApplicationError
from src.domain.team.team import Team
from src.domain.team.team_not_found_error import TeamNotFoundError

team_name = "F.C. Barcelona"
player_name = "Messi"
team_id = uuid.UUID("e154e156-6d6f-402f-b571-d83fc7d605f2")


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True

    yield app


@pytest.fixture
def db():
    db_handler = Container.database_handler()
    db = db_handler.get_database()
    db.teams.delete_many({})
    yield db_handler
    db.teams.delete_many({})


@pytest.fixture
def client(app, db):
    with app.app_context():
        with app.test_client() as client:
            yield client


class TestCreateTeamEndpoint:
    def test_should_return_400_when_name_field_is_missing(self, client):
        result = client.post('/teams', json={})

        assert result.status_code == 400
        assert result.json == {
            'message': "Field 'name' is a required property"
        }

    def test_should_return_400_when_invalid_type_name_field(self, client):
        result = client.post('/teams', json={"name": 123})

        assert result.status_code == 400
        assert result.json == {
            'message': "Field 'name' has no correct format"
        }

    def test_should_return_422_when_there_is_application_error(self, client):
        with patch.object(CreateTeam, 'execute') as execute_mock:
            execute_mock.side_effect = ApplicationError("error")
            result = client.post('/teams', json={"name": "F.C. Barcelona"})

            assert result.status_code == 422
            assert result.json == {'message': "error"}
            execute_mock.assert_called_once()

    def test_should_return_500_when_there_is_a_server_error(self, client):
        with patch.object(CreateTeam, 'execute') as execute_mock:
            execute_mock.side_effect = Exception("error")
            result = client.post('/teams', json={"name": "F.C. Barcelona"})

            execute_mock.assert_called_once()
            assert result.status_code == 500
            assert result.json == {'message': "Internal server error"}

    def test_should_return_201_when_team_created(self, client):
        result = client.post('/teams', json={"name": "F.C. Barcelona"})

        assert result.status_code == 201


class TestSignPlayerEndpoint:
    def test_should_return_404_when_team_is_not_found(self, client):
        with patch.object(SignPlayer, 'execute') as execute_mock:
            execute_mock.side_effect = TeamNotFoundError("error")
            result = client.post('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2/players', json={"name": player_name})

            assert result.status_code == 404
            assert result.json == {'message': "error"}
            execute_mock.assert_called_once()

    def test_should_return_422_when_there_is_application_error(self, client):
        with patch.object(SignPlayer, 'execute') as execute_mock:
            execute_mock.side_effect = ApplicationError("error")
            result = client.post('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2/players', json={"name": player_name})

            assert result.status_code == 422
            assert result.json == {'message': "error"}
            execute_mock.assert_called_once()

    def test_should_return_500_when_there_is_internal_error(self, client):
        with patch.object(SignPlayer, 'execute') as execute_mock:
            execute_mock.side_effect = Exception("error")
            result = client.post('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2/players', json={"name": player_name})

            assert result.status_code == 500
            assert result.json == {'message': "Internal server error"}
            execute_mock.assert_called_once()

    def test_should_return_201_when_player_signed(self, client):
        team = Team.create(name=team_name, id=team_id)
        Container.team_repository().save(team)

        result = client.post('/teams/%s/players' % str(team_id), json={"name": player_name})

        assert result.status_code == 201


class TestGetTeamGetEndpoint:
    def test_should_return_404_when_team_is_not_found(self, client):
        with patch.object(GetTeam, 'execute') as execute_mock:
            execute_mock.side_effect = TeamNotFoundError("error")
            result = client.get('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2')

            assert result.status_code == 404
            assert result.json == {'message': "error"}
            execute_mock.assert_called_once()

    def test_should_return_422_when_there_is_application_error(self, client):
        with patch.object(GetTeam, 'execute') as execute_mock:
            execute_mock.side_effect = ApplicationError("error")
            result = client.get('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2')

            assert result.status_code == 422
            assert result.json == {'message': "error"}
            execute_mock.assert_called_once()

    def test_should_return_500_when_there_is_internal_error(self, client):
        with patch.object(GetTeam, 'execute') as execute_mock:
            execute_mock.side_effect = Exception("error")
            result = client.get('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2')

            assert result.status_code == 500
            assert result.json == {'message': "Internal server error"}
            execute_mock.assert_called_once()

    def test_should_return_200_when_retrieving_given_team(self, client):
        team = Team.create(name=team_name, id=team_id)
        team.sign_player(player_name)
        Container.team_repository().save(team)
        result = client.get('/teams/e154e156-6d6f-402f-b571-d83fc7d605f2')

        assert result.status_code == 200
        assert result.json == {
            'id': str(team_id),
            'name': team_name,
            'created_at': team.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'players': [
                {
                    'name': team.players[0].name,
                    'created_at': team.players[0].created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            ]
        }
