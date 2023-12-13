from abc import abstractmethod
from domain.team.team import Team


class TeamRepository:
    @abstractmethod
    def save(self, team: Team) -> str: raise NotImplementedError
