from abc import ABC, abstractmethod
from typing import Any


class DatabaseHandler(ABC):
    @abstractmethod
    def getDatabase(self) -> Any: raise NotImplementedError
