from abc import abstractmethod
from uuid import UUID

from domain.team.team import Team


class TeamRepository:
    @abstractmethod
    def save(self, team: Team) -> str: raise NotImplementedError
    @abstractmethod
    def find(self, id: UUID) -> Team: raise NotImplementedError
