import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.domain.core.invalid_domain_entity_error import InvalidDomainEntityError


class DomainEntity(ABC):
    @abstractmethod
    def __init__(self, id: Optional[UUID] = None, created_at: Optional[datetime] = None):
        self.id = id or uuid.uuid4()
        self.created_at = created_at or datetime.now()

    @property
    def id(self) -> UUID:
        return self.__id

    @id.setter
    def id(self, id: UUID) -> None:
        if not isinstance(id, UUID):
            raise InvalidDomainEntityError("Field id must be a valid UUID type")
        self.__id = id

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at: datetime) -> None:
        if not isinstance(created_at, datetime):
            raise InvalidDomainEntityError("Field created_at must be a valid datetime type")
        self.__created_at = created_at

    def to_object(self) -> dict:
        return {
            "id": str(self.id),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
