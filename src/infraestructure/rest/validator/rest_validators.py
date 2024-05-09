from functools import wraps
from jsonschema import validate

from src.infraestructure.rest.contracts.base_request_contract import BaseRequestContract


def validate_request_body(request, request_contract: BaseRequestContract):
    def validate_request_body_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            validate(request.get_json(), request_contract.contract())
            return f(*args, **kwargs)

        return wrapped
    return validate_request_body_decorator
