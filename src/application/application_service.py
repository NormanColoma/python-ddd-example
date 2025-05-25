from abc import ABC, abstractmethod

from src.application.application_command import ApplicationCommand
from src.application.application_response import ApplicationResponse


class ApplicationService(ABC):
    @abstractmethod
    def execute(self, command: ApplicationCommand) -> ApplicationResponse | None:
        raise NotImplementedError
