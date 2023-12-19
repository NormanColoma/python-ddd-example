from application.application_command import ApplicationCommand


class AddTeamCommand(ApplicationCommand):
    def __init__(self, name: str):
        self.__name = name

    def getFields(self):
        return {
            'name': self.__name,
        }
