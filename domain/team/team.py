import uuid
from datetime import datetime
from uuid import UUID

from domain.domain_entity import DomainEntity
from domain.team.invalid_team_error import InvalidTeamError


class Team(DomainEntity):
    def __init__(self, name, id: UUID, created_at: datetime):
        super().__init__(id, created_at)
        self.name = name
        self.players = []

    @classmethod
    def create(cls, name: str) -> 'Team':
        return cls(
            name=name,
            id=uuid.uuid4(),
            created_at=datetime.now())

    @classmethod
    def build(cls, name: str, id: UUID, created_at: datetime) -> 'Team':
        return cls(
            name=name,
            id=id,
            created_at=created_at)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        if name is None:
            raise InvalidTeamError('Field name cannot be set to empty')
        if not isinstance(name, str):
            raise InvalidTeamError('Field name must be a valid string type')
        self.__name = name

    def add_player(self, player):
        self.players.append(player)

    def __str__(self):
        return self.name

    def to_object(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at
        }
