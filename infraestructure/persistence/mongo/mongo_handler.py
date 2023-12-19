from typing import Any
from pymongo import MongoClient, IndexModel
from infraestructure.config.config import Config
from infraestructure.persistence.database_handler import DatabaseHandler


class MongoHandler(DatabaseHandler):
    def __init__(self, config: Config):
        self.__config = config
        self.__initialize()

    def getDatabase(self) -> Any:
        db_uri = self.__config.MONGO_URI
        db_name = self.__config.DB_NAME
        return MongoClient(db_uri, uuidRepresentation='standard')[db_name]

    def __initialize(self) -> None:
        db = self.getDatabase()
        name_index = IndexModel([("name", 1)], name="name")
        db.teams.create_indexes([name_index])
