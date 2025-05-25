import uuid
from datetime import datetime

from src.domain.core.domain_entity import DomainEntity
from src.domain.player.invalid_player_error import InvalidPlayerError


class Player(DomainEntity):
    def __init__(self, name: str, id: uuid.UUID, created_at: datetime):
        super().__init__(id, created_at)
        self.name = name

    @classmethod
    def create(cls, name: str) -> "Player":
        return cls(name=name, id=uuid.uuid4(), created_at=datetime.now())

    @classmethod
    def build(cls, name: str, id: uuid.UUID, created_at: datetime) -> "Player":
        return cls(name=name, id=id, created_at=created_at)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if name is None:
            raise InvalidPlayerError("Field name cannot be set to empty")
        if not isinstance(name, str):
            raise InvalidPlayerError("Field name must be a valid string type")
        self.__name = name

    def __str__(self):
        return self.name

    def __eq__(self, other: "Player") -> bool:
        return self.name == other.name and self.id == other.id and self.created_at == other.created_at

    def to_object(self) -> dict:
        return {
            **super().to_object(),
            "name": self.name,
        }
