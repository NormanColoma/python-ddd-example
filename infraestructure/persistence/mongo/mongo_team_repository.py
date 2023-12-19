import logging
from uuid import UUID

import pinject
from domain.team.team import Team
from domain.team.team_repository import TeamRepository
from infraestructure.persistence.database_handler import DatabaseHandler
from infraestructure.persistence.database_parser import DatabaseParser
from infraestructure.persistence.mongo.mongo_team_parser import MongoTeamParser


class MongoTeamRepository(TeamRepository):
    @pinject.annotate_arg('database_parser', 'team_parser')
    def __init__(self, database_handler: DatabaseHandler, database_parser: DatabaseParser):
        self.__db = database_handler.getDatabase()
        self.__team_parser: DatabaseParser = database_parser

    def save(self, team: Team) -> None:
        document: dict = self.__team_parser.to_database_object(team)
        self.__db.teams.insert_one(document)

    def find(self, id: UUID) -> Team:
        document: dict = dict()
        try:
            document = self.__db.teams.find_one({'_id': id})
        except Exception as e:
            logging.info(e)

        return self.__team_parser.to_domain_object(document)
