from functools import wraps
from flask import Flask
from infraestructure.rest.team_controller import team_controller

app = Flask(__name__)
app.register_blueprint(team_controller)


def has_permissions(permission):
    def decorated_function(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if permission == 'read':
                print('has permissions')
                return f(*args, **kwargs)

        return wrapped

    return decorated_function


if __name__ == '__main__':
    app.run()
