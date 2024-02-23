import os

from dependency_injector import containers, providers

from application.add_player_to_team.add_player_to_team import AddPlayerToTeam
from application.add_team.add_team import AddTeam
from application.get_team.get_team import GetTeam
from infraestructure.bus.event.fake_event_bus import FakeEventBus
from infraestructure.config.config import app_config
from infraestructure.persistence.mongo.mongo_handler import MongoHandler
from infraestructure.persistence.mongo.mongo_team_parser import MongoTeamParser
from infraestructure.persistence.mongo.mongo_team_repository import MongoTeamRepository


class Container(containers.DeclarativeContainer):
    database_handler = providers.Singleton(
        MongoHandler,
        config=app_config[os.getenv('ENV')]
    )

    database_parser = providers.Singleton(MongoTeamParser)

    event_bus = providers.Singleton(FakeEventBus)

    team_repository = providers.Singleton(
        MongoTeamRepository,
        database_handler,
        database_parser,
    )

    add_team = providers.Singleton(
        AddTeam,
        team_repository,
        event_bus,
    )

    get_team = providers.Singleton(
        GetTeam,
        team_repository
    )

    add_player_to_team = providers.Singleton(
        AddPlayerToTeam,
        team_repository,
        event_bus
    )

