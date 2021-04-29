from flask.views import MethodView
from flask import request
from http import HTTPStatus
from global_objects import db
from helpers.customflask import ApiException


class MsgAPI(MethodView):
    """The MsgApi class implements a post and a get method to
    insert and retrieve messages from mongodb."""

    def get(self):
        return db.connection.test.messages.find()

    def post(self):
        if not request.data:
            raise ApiException("request body cannot be empty")
        content = request.get_json(silent=True)
        msg = content.get("message")
        if not msg:
            raise ApiException(
                "message field is required", HTTPStatus.UNPROCESSABLE_ENTITY
            )
        result = db.connection.test.messages.insert_one({"message": msg})
        return {"oid": str(result.inserted_id)}, HTTPStatus.CREATED
