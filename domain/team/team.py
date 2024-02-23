from datetime import datetime
from uuid import UUID
from domain.core.aggregate_root import AggregateRoot
from domain.player.player import Player
from domain.team.invalid_team_error import InvalidTeamError
from domain.team.team_created_event import TeamCreatedEvent
from domain.team.team_modified_event import TeamModifiedEvent


class Team(AggregateRoot):
    def __init__(self, name, id: UUID, created_at: datetime):
        super().__init__(id, created_at)
        self.name = name
        self.players = []

    @classmethod
    def create(cls, name: str, id: UUID) -> 'Team':
        team: Team = cls(
            name=name,
            id=id,
            created_at=datetime.now())
        team.add_event(TeamCreatedEvent(entity=team))

        return team

    @classmethod
    def build(cls, name: str, id: UUID, created_at: datetime, players: [Player]) -> 'Team':
        team = cls(
            name=name,
            id=id,
            created_at=created_at)
        team.players = players
        return team

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

    def add_player(self, player_name: str) -> None:
        if len(self.players) >= 11:
            raise InvalidTeamError('Team already has 11 players')
        player = Player.create(player_name)
        self.players.append(player)
        self.add_event(TeamModifiedEvent(entity=self))

    def to_object(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at
        }

    def __eq__(self, other):
        if isinstance(other, Team):
            return self.id == other.id
        return False

    def __str__(self):
        return self.name

