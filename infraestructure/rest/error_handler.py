import json
from flask import Response
from jsonschema.exceptions import ValidationError


def handle_exception(e):
    if isinstance(e, ValidationError):
        if e.validator == 'required':
            error_message = {
                'message': e.message,
            }
            return Response(response=json.dumps(error_message), status=400, mimetype='application/json')
        elif e.validator == 'type':
            error_message = {
                'message': e.message,
            }
            return Response(response=json.dumps(error_message), status=400, mimetype='application/json')
    return Response(status=500, mimetype='application/json')
