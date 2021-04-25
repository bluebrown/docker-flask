from flask import Blueprint, jsonify, request, Response, abort, current_app as app
from bson.json_util import dumps
from pymongo import errors


def create(client):
    main = Blueprint("main", __name__)
    messages = client.test.messages

    @main.route("/")
    def index():
        try:
            msgs = messages.find()
        except errors.ServerSelectionTimeoutError as timeout:
            app.log_exception(timeout)
            abort(503)
        except Exception as generic:
            app.log_exception(generic)
            abort(500)

        return Response(dumps(msgs), content_type="application/json")

    @main.route("/msg", methods=["POST"])
    def msg():
        if not request.data:
            abort(400)
        content = request.get_json(silent=True)
        app.logger.debug(f"message posted: {content}")
        try:
            result = messages.insert_one({"message": content.get("message")})
        except errors.ServerSelectionTimeoutError as timeout:
            app.log_exception(timeout)
            abort(503)
        except Exception as generic:
            app.log_exception(generic)
            abort(400)
        payload = jsonify(id=str(result.inserted_id))
        app.logger.debug(f"payload: {payload}")
        return payload, 201

    return main
