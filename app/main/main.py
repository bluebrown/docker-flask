from flask import Blueprint, jsonify, request, Response, current_app as app
from bson.json_util import dumps


def create(client):
    main = Blueprint("main", __name__)
    messages = client.test.messages

    @main.route("/")
    def index():
        msgs = messages.find()
        return Response(dumps(msgs), content_type="application/json")

    @main.route("/msg", methods=["POST"])
    def msg():
        content = request.get_json(silent=True)
        app.logger.info(f"message posted: {content}")
        result = messages.insert_one({"message": content.get("message")})
        payload = jsonify(id=str(result.inserted_id))
        app.logger.debug(f"payload: {payload}")
        return payload, 201

    return main
