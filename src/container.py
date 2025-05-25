import os

from dependency_injector import containers, providers

from src.application.create_team.create_team import CreateTeam
from src.application.get_team.get_team import GetTeam
from src.application.sign_player.sign_player import SignPlayer
from src.infraestructure.bus.event.consumer.team_created_consumer import TeamCreatedConsumer
from src.infraestructure.bus.event.kafka_event_bus import KafkaEventBus
from src.infraestructure.bus.event.kafka_producer import KafkaProducer
from src.infraestructure.bus.event.kafka_topic_creator import KafkaTopicCreator
from src.infraestructure.config.config import app_config
from src.infraestructure.persistence.mongo.mongo_handler import MongoHandler
from src.infraestructure.persistence.mongo.mongo_team_parser import MongoTeamParser
from src.infraestructure.persistence.mongo.mongo_team_repository import MongoTeamRepository
from src.infraestructure.rest.team_controller import TeamController


class Container(containers.DeclarativeContainer):
    # infra services
    database_handler = providers.Singleton(MongoHandler, config=app_config[os.getenv("ENV") or "test"])

    database_parser = providers.Singleton(MongoTeamParser)

    topic_creator = providers.Singleton(KafkaTopicCreator, config=app_config[os.getenv("ENV") or "test"])
    producer = providers.Singleton(KafkaProducer, config=app_config[os.getenv("ENV") or "test"])

    team_created_consumer = providers.Singleton(TeamCreatedConsumer, config=app_config[os.getenv("ENV") or "test"])

    event_bus = providers.Singleton(
        KafkaEventBus, producer=producer, topic_creator=topic_creator, consumers=[team_created_consumer]
    )

    # repositories
    team_repository = providers.Singleton(
        MongoTeamRepository,
        database_handler,
        database_parser,
    )

    # application services

    create_team = providers.Singleton(
        CreateTeam,
        team_repository,
        event_bus,
    )

    get_team = providers.Singleton(GetTeam, team_repository)

    sign_player = providers.Singleton(SignPlayer, team_repository, event_bus)

    # controllers
    team_controller = providers.Singleton(TeamController, get_team, create_team, sign_player)
