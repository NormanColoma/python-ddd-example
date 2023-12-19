from uuid import UUID

from application.application_command import ApplicationCommand


class GetTeamCommand(ApplicationCommand):
    def __init__(self, id: UUID):
        self.__id = id

    def getFields(self):
        return {
            'id': self.__id,
        }
