from flask import Blueprint, request, Response
from application.add_team_command import AddTeamCommand
from container import obj_graph, AddTeam
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
