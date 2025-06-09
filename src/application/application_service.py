from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.application.application_command import ApplicationCommand
from src.application.application_response import ApplicationResponse

C = TypeVar("C", bound=ApplicationCommand)
R = TypeVar("R", bound=ApplicationResponse)


class ApplicationService(ABC, Generic[C, R]):
    @abstractmethod
    def execute(self, command: C) -> R | None:
        raise NotImplementedError
