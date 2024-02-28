from uuid import UUID

from src.application.application_command import ApplicationCommand


class GetTeamCommand(ApplicationCommand):
    def __init__(self, id: UUID):
        self.__id = id

    @property
    def id(self) -> UUID:
        return self.__id
