import uuid
from datetime import datetime

import pytest
from freezegun import freeze_time

from src.domain.team.invalid_team_error import InvalidTeamError
from src.domain.team.team import Team


@freeze_time("2012-01-01")
class TestTeamDomainEntity:
    id = uuid.uuid4()
    name = 'team'
    created_at = datetime.now()

    def test_should_raise_exception_when_name_is_empty(self):
        with pytest.raises(InvalidTeamError) as e:
            Team.create(name=None, id=self.id)
        assert e.value.message == 'Field name cannot be set to empty'

    def test_should_raise_exception_when_name_is_not_string(self):
        with pytest.raises(InvalidTeamError) as e:
            Team.create(name=12, id=self.id)
        assert e.value.message == 'Field name must be a valid string type'

    def test_should_create_team(self, mocker):
        mocker.patch('uuid.uuid4', return_value=self.id)
        mocker.patch('datetime.datetime.now', return_value=self.created_at)
        team = Team.create(name=self.name, id=self.id)

        assert team.id == self.id
        assert team.name == self.name
        assert team.created_at == self.created_at
        assert team.players == []

    def test_should_build_team(self):
        team = Team.build(name=self.name, id=self.id, created_at=self.created_at, players=[])

        assert team.id == self.id
        assert team.name == self.name
        assert team.created_at == self.created_at
        assert team.players == []

    def test_should_sign_player(self):
        team = Team.build(name=self.name, id=self.id, created_at=self.created_at, players=[])

        team.sign_player('player_name')

        assert len(team.players) == 1
        assert team.players[0].name == 'player_name'

    def test_should_raise_exception_when_signing_a_player(self):
        team = Team.build(name=self.name, id=self.id, created_at=self.created_at, players=[])

        number_of_players = 0
        while number_of_players < 11:
            team.sign_player('player_name')
            number_of_players += 1

        with pytest.raises(InvalidTeamError) as e:
            team.sign_player('player_name')
        assert e.value.message == 'Team already has 11 players'

    def test_should_print_team_as_object(self):
        team = Team.build(name=self.name, id=self.id, created_at=self.created_at, players=[])
        expected_team = {
            'id': str(self.id),
            'name': self.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'players': []
        }

        assert team.to_object() == expected_team
