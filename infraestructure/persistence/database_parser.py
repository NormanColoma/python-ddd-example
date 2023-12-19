from abc import ABC, abstractmethod
from typing import Any

from domain.domain_entity import DomainEntity


class DatabaseParser(ABC):
    @abstractmethod
    def to_database_object(self, domain: DomainEntity) -> dict: raise NotImplementedError

    @abstractmethod
    def to_domain_object(self, database_object: dict) -> Any: raise NotImplementedError
