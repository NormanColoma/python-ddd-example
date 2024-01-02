import os

import pinject
from pymongo import MongoClient

from application.add_player_to_team.add_player_to_team import AddPlayerToTeam
from application.add_team.add_team import AddTeam
from application.get_team.get_team import GetTeam
from infraestructure.config.config import app_config
from infraestructure.persistence.mongo.mongo_handler import MongoHandler
from infraestructure.persistence.mongo.mongo_team_parser import MongoTeamParser
from infraestructure.persistence.mongo.mongo_team_repository import MongoTeamRepository


class MongoClientInstance(pinject.BindingSpec):
    def provide_database_handler(self):
        env = os.getenv('ENV') or 'run'
        db_uri = app_config[env].MONGO_URI
        return MongoClient(db_uri)


class DatabaseHandlerInstance(pinject.BindingSpec):
    def provide_database_handler(self):
        return obj_graph.provide(MongoHandler)


class DatabaseParser(pinject.BindingSpec):
    def configure(self, bind):
        bind('database_parser', annotated_with='team_parser', to_class=MongoTeamParser)


class Config(pinject.BindingSpec):
    def provide_config(self):
        env = os.getenv('ENV') or 'run'
        return app_config[env]


class TeamRepository(pinject.BindingSpec):
    def provide_team_repository(self):
        return obj_graph.provide(MongoTeamRepository)


class AddTeamUseCase(pinject.BindingSpec):
    def provide_add_team(self):
        return obj_graph.provide(AddTeam)


class AddPlayerToTeamUseCase(pinject.BindingSpec):
    def provide_add_player_to_team(self):
        return obj_graph.provide(AddPlayerToTeam)


class GetTeamUseCase(pinject.BindingSpec):
    def provide_get_team(self):
        return obj_graph.provide(GetTeam)


obj_graph = pinject.new_object_graph(modules=None,
                                     binding_specs=[DatabaseHandlerInstance(), TeamRepository(),
                                                    DatabaseParser(), Config(), AddTeamUseCase(), GetTeamUseCase(),
                                                    AddPlayerToTeamUseCase()])
