from abc import ABC, abstractmethod
from typing import Any


class DatabaseHandler(ABC):
    @abstractmethod
    def get_database(self) -> Any: raise NotImplementedError
