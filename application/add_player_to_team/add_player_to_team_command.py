from uuid import UUID

from application.application_command import ApplicationCommand


class AddPlayerToTeamCommand(ApplicationCommand):
    def __init__(self, player_name: str, team_id: UUID):
        self.__player_name= player_name
        self.__team_id = team_id

    def getFields(self):
        return {
            'player_name': self.__player_name,
            'team_id': self.__team_id,
        }
