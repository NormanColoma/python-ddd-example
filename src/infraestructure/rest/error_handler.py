import json
import logging

from flask import Response
from jsonschema.exceptions import ValidationError

from src.domain.core.applicaton_error import ApplicationError


def handle_exception(e):
    error = e.args[0] if len(e.args) > 0 else "unknown error"
    logging.info(type(e).__name__ + " due to: " + error)
    if isinstance(e, ValidationError):
        if e.validator == "required":
            error_message = {
                "message": "Field %s" % error,
            }
            return Response(response=json.dumps(error_message), status=400, mimetype="application/json")
        elif e.validator == "type":
            error_message = {"message": "Field '%s' has no correct format" % e.path[0]}
            return Response(response=json.dumps(error_message), status=400, mimetype="application/json")
    elif isinstance(e, ApplicationError):
        return Response(status=422, response=json.dumps({"message": error}), mimetype="application/json")
    return Response(response=json.dumps({"message": "Internal server error"}), status=500, mimetype="application/json")
