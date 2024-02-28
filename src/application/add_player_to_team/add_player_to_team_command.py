from uuid import UUID

from src.application.application_command import ApplicationCommand


class AddPlayerToTeamCommand(ApplicationCommand):
    def __init__(self, player_name: str, team_id: UUID):
        self.__player_name= player_name
        self.__team_id = team_id

    @property
    def team_id(self) -> UUID:
        return self.__team_id

    @property
    def player_name(self) -> str:
        return self.__player_name
