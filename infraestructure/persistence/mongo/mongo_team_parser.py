import bson

from domain.team.team import Team
from infraestructure.persistence.database_parser import DatabaseParser


class MongoTeamParser(DatabaseParser):
    def to_domain_object(self, database_object: dict) -> Team:
        return Team.build(database_object['name'], database_object['_id'], database_object['created_at'])

    def to_database_object(self, domain: Team) -> dict:
        document = dict()
        document['_id'] = bson.Binary.from_uuid(domain.id)
        document['name'] = domain.name
        document['created_at'] = domain.created_at

        return document
