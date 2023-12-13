from functools import wraps
from flask import Flask
from application.add_team import AddTeam
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
    add_team = obj_graph.provide(AddTeam)
    add_team.save()


if __name__ == '__main__':
    app.run()
