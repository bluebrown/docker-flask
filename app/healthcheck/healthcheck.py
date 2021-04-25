from flask import Response, Blueprint, abort, current_app as app


def create(client):
    healthcheck = Blueprint("healthcheck", __name__)

    @healthcheck.route("/alive")
    def livelyness():
        return Response(status=200)

    @healthcheck.route("/ready")
    def readyness():
        return Response(status=200) if isAlive(client) else abort(503)

    return healthcheck


def isAlive(client):
    try:
        app.logger.debug("trying")
        client.server_info()
        return True
    except Exception as e:
        app.logger.error(e)
        return False
