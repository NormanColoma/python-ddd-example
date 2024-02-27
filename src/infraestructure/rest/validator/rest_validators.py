from functools import wraps
from jsonschema import validate


def validate_request_body(request, request_contract):
    def validate_request_body_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            validate(request.get_json(), request_contract)
            return f(*args, **kwargs)

        return wrapped
    return validate_request_body_decorator
