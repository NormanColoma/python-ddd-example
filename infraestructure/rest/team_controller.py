import json
import uuid

from flask import Blueprint, request, Response

from application.add_team.add_team_command import AddTeamCommand
from application.get_team.get_team_command import GetTeamCommand
from application.get_team.get_team_response import GetTeamResponse
from container import obj_graph, GetTeam, AddTeam
from infraestructure.rest.validator.rest_validators import validate_request_body

team_controller = Blueprint('team_controller', __name__)

post_request_contract = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
    },
    'required': ['name']
}


@team_controller.route('/', methods=["POST"])
@validate_request_body(request, request_contract=post_request_contract)
def add_team_route():
    body = request.get_json()

    add_team = obj_graph.provide(AddTeam)
    command = AddTeamCommand(**body)
    add_team.save(command)
    return Response(status=201, mimetype='application/json')


@team_controller.route('/<team_id>', methods=["GET"])
def get_team_route(team_id: str):
    get_team = obj_graph.provide(GetTeam)
    command = GetTeamCommand(uuid.UUID(team_id))

    response: GetTeamResponse = get_team.get(command)
    return Response(response=json.dumps(response.toJSON()), status=200, mimetype='application/json')
