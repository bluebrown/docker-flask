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


class MsgAPI(MethodView):
    def get(self):
        try:
            msgs = get_db().test.messages.find()
        except errors.ServerSelectionTimeoutError as timeout:
            app.log_exception(timeout)
            abort(503)
        except Exception as generic:
            app.log_exception(generic)
            abort(500)
        return Response(dumps(msgs), content_type="application/json")

    def post(self):
        if not request.data:
            abort(400)
        content = request.get_json(silent=True)
        app.logger.debug(f"message posted: {content}")
        try:
            result = get_db().test.messages.insert_one(
                {"message": content.get("message")}
            )
        except errors.ServerSelectionTimeoutError as timeout:
            app.log_exception(timeout)
            abort(503)
        except Exception as generic:
            app.log_exception(generic)
            abort(400)
        payload = jsonify(id=str(result.inserted_id))
        app.logger.debug(f"payload: {payload}")
        return payload, 201
