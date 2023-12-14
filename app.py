from functools import wraps
from flask import Flask, request, Response
from application.add_team import AddTeam
from application.add_team_command import AddTeamCommand
from container import obj_graph

app = Flask(__name__)


def has_permissions(permission):
    def decorated_function(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if permission == 'read':
                print('has permissions')
                return f(*args, **kwargs)

        return wrapped

    return decorated_function


@app.route('/', methods=["POST"])
# @has_permissions('read')
def add_team_route():
    body = request.get_json()

    add_team = obj_graph.provide(AddTeam)
    command = AddTeamCommand(**body)
    add_team.save(command)
    return Response(status=201, mimetype='application/json')


if __name__ == '__main__':
    app.run()
