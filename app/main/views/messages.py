from flask.views import MethodView
from flask import (
    jsonify,
    request,
    Response,
    abort,
    current_app as app,
)
from bson.json_util import dumps
from pymongo import errors
from extensions import get_db
from http import HTTPStatus


class MsgAPI(MethodView):
    def get(self):
        try:
            msgs = get_db().test.messages.find()
        except errors.ServerSelectionTimeoutError as timeout:
            app.log_exception(timeout)
            abort(HTTPStatus.SERVICE_UNAVAILABLE)
        except Exception as generic:
            app.log_exception(generic)
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)
        return Response(dumps(msgs), content_type="application/json")

    def post(self):
        if not request.data:
            abort(HTTPStatus.BAD_REQUEST)
        content = request.get_json(silent=True)
        app.logger.debug(f"message posted: {content}")
        msg = content.get("message", None)
        if not msg:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY)
        try:
            result = get_db().test.messages.insert_one({"message": msg})
        except errors.ServerSelectionTimeoutError as timeout:
            app.log_exception(timeout)
            abort(HTTPStatus.SERVICE_UNAVAILABLE)
        except Exception as generic:
            app.log_exception(generic)
            abort(HTTPStatus.BAD_REQUEST)
        payload = jsonify(id=str(result.inserted_id))
        app.logger.debug(f"payload: {payload}")
        return payload, HTTPStatus.CREATED
