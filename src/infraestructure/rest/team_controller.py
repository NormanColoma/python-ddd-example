import json
import logging
import uuid

from flask import Blueprint, Response, request

from src.application.application_response import ApplicationResponse
from src.application.create_team.create_team import CreateTeam
from src.application.create_team.create_team_command import CreateTeamCommand
from src.application.get_team.get_team import GetTeam
from src.application.get_team.get_team_command import GetTeamCommand
from src.application.sign_player.sign_player import SignPlayer
from src.application.sign_player.sign_player_command import SignPlayerCommand
from src.domain.team.team_not_found_error import TeamNotFoundError
from src.infraestructure.rest.base_controller import BaseController
from src.infraestructure.rest.contracts.add_team_request_contract import AddTeamRequestContract
from src.infraestructure.rest.contracts.sign_player_request_contract import SignPlayerRequestContract
from src.infraestructure.rest.validator.rest_validators import validate_request_body


class TeamController(BaseController):
    def __init__(self, get_team: GetTeam, create_team: CreateTeam, sign_player: SignPlayer):
        self.register_routes()
        self.__get_team = get_team
        self.__create_team = create_team
        self.__sign_player = sign_player

    @validate_request_body(request, request_contract=AddTeamRequestContract)
    def create_team_route(self):
        body = request.get_json()
        command = CreateTeamCommand(**body)
        self.__create_team.execute(command)
        return Response(status=201, mimetype="application/json")

    @validate_request_body(request, request_contract=SignPlayerRequestContract)
    def sign_player_route(self, team_id: str):
        try:
            body = request.get_json()

            command = SignPlayerCommand(player_name=body["name"], team_id=uuid.UUID(team_id))
            self.__sign_player.execute(command)
            return Response(status=201, mimetype="application/json")
        except Exception as e:
            if isinstance(e, TeamNotFoundError):
                return Response(response=json.dumps({"message": e.message}), status=404, mimetype="application/json")
            raise e

    def get_team_route(self, team_id: str):
        try:
            command = GetTeamCommand(uuid.UUID(team_id))
            response: ApplicationResponse = self.__get_team.execute(command)
            return Response(response=json.dumps(response.to_json()), status=200, mimetype="application/json")
        except Exception as e:
            if isinstance(e, TeamNotFoundError):
                logging.info(e.message)
                return Response(response=json.dumps({"message": e.message}), status=404, mimetype="application/json")
            raise e

    def register_routes(self):
        self.__routes = Blueprint("team_controller", __name__)

        self.__routes.add_url_rule("/<team_id>", "get_team_route", self.get_team_route, methods=["GET"])
        self.__routes.add_url_rule("", "create_team_route", self.create_team_route, methods=["POST"])
        self.__routes.add_url_rule("/<team_id>/players", "sign_player_route", self.sign_player_route, methods=["POST"])

    def routes(self):
        return self.__routes
