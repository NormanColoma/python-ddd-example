from abc import abstractmethod
from typing import Optional
from uuid import UUID
from domain.team.team import Team


class TeamRepository:
    @abstractmethod
    def save(self, team: Team) -> None: raise NotImplementedError

    @abstractmethod
    def find(self, id: UUID) -> Optional[Team]: raise NotImplementedError
