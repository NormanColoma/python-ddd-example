from abc import ABC, abstractmethod

from application.application_command import ApplicationCommand
from application.application_response import ApplicationResponse


class ApplicationService(ABC):
    @abstractmethod
    def execute(self, command: ApplicationCommand) -> ApplicationResponse | None: raise NotImplementedError
