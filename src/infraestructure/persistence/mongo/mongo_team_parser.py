import uuid
from typing import List

import bson

from src.domain.player.player import Player
from src.domain.team.team import Team
from src.infraestructure.persistence.database_parser import DatabaseParser


class MongoTeamParser(DatabaseParser):
    def to_domain_object(self, database_object: dict) -> Team:
        players: List[Player] = [
            Player.build(player["name"], uuid.UUID(player["id"]), player["created_at"])
            for player in database_object["players"]
        ]
        return Team.build(database_object["name"], database_object["_id"], database_object["created_at"], players)

    def to_database_object(self, domain: Team) -> dict:
        document = dict()
        document["_id"] = bson.Binary.from_uuid(domain.id)
        document["name"] = domain.name
        document["created_at"] = domain.created_at
        document["players"] = [
            {
                "id": str(player.id),
                "name": player.name,
                "created_at": player.created_at,
            }
            for player in domain.players
        ]

        return document
