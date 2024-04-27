from abc import ABC, abstractmethod
from typing import Any


class BaseController(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def register_routes(self) -> None:
        pass

    @abstractmethod
    def routes(self) -> Any:
        pass
