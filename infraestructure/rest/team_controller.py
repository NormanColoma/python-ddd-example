from flask import Blueprint, request, Response

from application.add_team import AddTeam
from application.add_team_command import AddTeamCommand
from container import obj_graph

team_controller = Blueprint('team_controller', __name__)


@team_controller.route('/', methods=["POST"])
# @has_permissions('read')
def add_team_route():
    body = request.get_json()

    add_team = obj_graph.provide(AddTeam)
    command = AddTeamCommand(**body)
    add_team.save(command)
    return Response(status=201, mimetype='application/json')
