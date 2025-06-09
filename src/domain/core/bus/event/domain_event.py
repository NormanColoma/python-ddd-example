import os
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic

from src.domain.types import E
from src.infraestructure.config.config import app_config


class DomainEvent(ABC, Generic[E]):
    @abstractmethod
    def __init__(self, entity: E, name: str):
        self.__id = uuid.uuid4()
        self.__occurred_at = datetime.now()
        self.__name = name
        self.__entity = entity
        self.__entity_name = entity.__class__.__name__
        self.__entity_id = entity.id
        self.topic = app_config[os.getenv("ENV")].TOPIC

    def to_json(self) -> dict:
        return {
            "id": str(self.__id),
            "name": self.__name,
            "entity": self.__entity.to_object(),
            "entity_name": self.__entity_name,
            "entity_id": str(self.__entity_id),
            "occurred_at": self.__occurred_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
