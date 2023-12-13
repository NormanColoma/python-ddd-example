import pinject

from domain.team.team import Team
from domain.team.team_repository import TeamRepository
from infraestructure.persistence.database_handler import DatabaseHandler
from infraestructure.persistence.database_parser import DatabaseParser


class MongoTeamRepository(TeamRepository):
    @pinject.annotate_arg('database_parser', 'team_parser')
    def __init__(self, database_handler: DatabaseHandler, database_parser: DatabaseParser):
        self.__db = database_handler.getDatabase()
        self.__team_parser: DatabaseParser = database_parser

    def save(self, team: Team) -> None:
        document: dict = self.__team_parser.to_database_object(team)
        self.__db.teams.insert_one(document)
