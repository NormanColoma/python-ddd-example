import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from src.domain.core.domain_entity import DomainEntity


class DomainEvent(ABC):
    @abstractmethod
    def __init__(self, entity: DomainEntity, name: str):
        self.__id = uuid.uuid4()
        self.__occurred_at = datetime.now()
        self.__name = name
        self.__entity = entity
        self.__entity_name = entity.__class__.__name__
        self.__entity_id = entity.id
        self.__topic__ = 'fake-topic'



