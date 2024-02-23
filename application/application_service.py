from abc import ABC, abstractmethod

from application.application_command import ApplicationCommand


class ApplicationService(ABC):
    @abstractmethod
    def execute(self, command: ApplicationCommand): raise NotImplementedError
