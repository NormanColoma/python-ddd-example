from functools import wraps

from application import use_case
from flask import Flask
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


@app.route('/<id>')
# @has_permissions('read')
def hello_world(id):
    test = obj_graph.provide(use_case.UseCase)
    return test.save()


if __name__ == '__main__':
    app.run()
