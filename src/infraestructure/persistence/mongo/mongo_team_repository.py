import logging
from types import NoneType
from typing import Optional
from uuid import UUID

from src.domain.team.team import Team
from src.domain.team.team_repository import TeamRepository
from src.infraestructure.persistence.database_handler import DatabaseHandler
from src.infraestructure.persistence.database_parser import DatabaseParser


class MongoTeamRepository(TeamRepository):
    def __init__(self, database_handler: DatabaseHandler, database_parser: DatabaseParser):
        self.__db = database_handler.get_database()
        self.__team_parser: DatabaseParser = database_parser

    def save(self, team: Team) -> None:
        document: dict = self.__team_parser.to_database_object(team)
        self.__db.teams.replace_one({'_id': team.id}, document, upsert=True)

    def find(self, id: UUID) -> Optional[Team]:
        document: dict = dict()
        try:
            document = self.__db.teams.find_one({'_id': id})
        except Exception as e:
            logging.info(e)

        return None if isinstance(document, NoneType) else self.__team_parser.to_domain_object(document)
