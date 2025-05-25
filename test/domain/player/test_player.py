import datetime
import uuid

import pytest
from freezegun import freeze_time

from src.domain.player.invalid_player_error import InvalidPlayerError
from src.domain.player.player import Player


@freeze_time("2012-01-01")
class TestPlayerDomainEntity:
    id = uuid.uuid4()
    name = "player"
    created_at = datetime.datetime.now()

    def test_should_raise_exception_when_name_is_empty(self):
        with pytest.raises(InvalidPlayerError) as e:
            Player.create(name=None)
        assert e.value.message == "Field name cannot be set to empty"

    def test_should_raise_exception_when_name_is_not_string(self):
        with pytest.raises(InvalidPlayerError) as e:
            Player.create(name=12)
        assert e.value.message == "Field name must be a valid string type"

    def test_should_build_a_player(self):
        player = Player.build(name=self.name, id=self.id, created_at=self.created_at)

        assert player.name == self.name
        assert player.id == self.id
        assert player.created_at == self.created_at

    def test_should_create_a_player(self, mocker):
        mocker.patch("uuid.uuid4", return_value=self.id)
        mocker.patch("datetime.datetime.now", return_value=self.created_at)
        player = Player.create(name=self.name)

        assert player.id == self.id
        assert player.name == self.name
        assert player.created_at == self.created_at

    def test_should_print_object_as_dict(self):
        player = Player.build(name=self.name, id=self.id, created_at=self.created_at)
        expected_player = {
            "id": str(self.id),
            "name": self.name,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

        assert player.to_object() == expected_player
