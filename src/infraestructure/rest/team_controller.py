import json
import uuid

from flask import Blueprint, request, Response, current_app
from src.application.add_player_to_team.add_player_to_team_command import AddPlayerToTeamCommand
from src.application.add_team.add_team import AddTeam
from src.application.add_team.add_team_command import AddTeamCommand
from src.application.application_response import ApplicationResponse
from src.application.get_team.get_team_command import GetTeamCommand
from src.domain.team.team_not_found_error import TeamNotFoundError
from src.infraestructure.rest.validator.rest_validators import validate_request_body

team_controller = Blueprint('team_controller', __name__)

post_request_contract = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
    },
    'required': ['name']
}


@team_controller.route('', methods=["POST"])
@validate_request_body(request, request_contract=post_request_contract)
def add_team_route():
    body = request.get_json()
    add_team: AddTeam = current_app.container.add_team()
    command = AddTeamCommand(**body)
    add_team.execute(command)
    return Response(status=201, mimetype='application/json')


@team_controller.route('/<team_id>/players', methods=["POST"])
@validate_request_body(request, request_contract=post_request_contract)
def add_player_to_team_route(team_id: str):
    try:
        body = request.get_json()
        add_player_to_team = current_app.container.add_player_to_team()

        command = AddPlayerToTeamCommand(player_name=body['name'], team_id=uuid.UUID(team_id))
        add_player_to_team.execute(command)
        return Response(status=201, mimetype='application/json')
    except Exception as e:
        if isinstance(e, TeamNotFoundError):
            return Response(response=json.dumps({'message': e.message}), status=404, mimetype='application/json')
        raise e


@team_controller.route('/<team_id>', methods=["GET"])
def get_team_route(team_id: str):
    try:
        get_team = current_app.container.get_team()
        command = GetTeamCommand(uuid.UUID(team_id))

        response: ApplicationResponse = get_team.execute(command)
        return Response(response=json.dumps(response.to_json()), status=200, mimetype='application/json')
    except Exception as e:
        if isinstance(e, TeamNotFoundError):
            return Response(response=json.dumps({'message': e.message}), status=404, mimetype='application/json')
        raise e