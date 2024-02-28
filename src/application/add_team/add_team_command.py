from src.application.application_command import ApplicationCommand


class AddTeamCommand(ApplicationCommand):
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name
