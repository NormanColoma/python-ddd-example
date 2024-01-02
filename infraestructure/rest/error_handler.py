import json
import logging

from flask import Response
from jsonschema.exceptions import ValidationError


def handle_exception(e):
    logging.info(type(e).__name__ + " due to: " + e.args[0])
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
    return Response(response=json.dumps({'message': 'Internal server error'}), status=500, mimetype='application/json')
