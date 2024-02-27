from abc import ABC, abstractmethod


class ApplicationResponse(ABC):
    @abstractmethod
    def to_json(self) -> dict: raise NotImplementedError
