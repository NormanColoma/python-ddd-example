import uuid
from datetime import datetime
from domain.core.domain_entity import DomainEntity
from domain.player.invalid_player_error import InvalidPlayerError


class Player(DomainEntity):
    def __init__(self, name, id, created_at):
        super().__init__(id, created_at)
        self.name = name

    @classmethod
    def create(cls, name):
        return cls(
            name=name,
            id=uuid.uuid4(),
            created_at=datetime.now())

    @classmethod
    def build(cls, name, id, created_at):
        return cls(
            name=name,
            id=id,
            created_at=created_at)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if name is None:
            raise InvalidPlayerError('Field name cannot be set to empty')
        if not isinstance(name, str):
            raise InvalidPlayerError('Field name must be a valid string type')
        self.__name = name

    def __str__(self):
        return self.name

    def to_object(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at
        }
