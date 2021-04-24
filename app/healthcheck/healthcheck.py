from flask import Response, Blueprint, abort, current_app as app


def create(client):
    healthcheck = Blueprint("healthcheck", __name__)

    @healthcheck.route("/alive")
    def livelyness():
        return Response(status=200)

    @healthcheck.route("/ready")
    def readyness():
        try:
            client.server_info()
            return Response(status=200)
        except Exception as e:
            app.logger.error(e)
            abort(503)

    return healthcheck
