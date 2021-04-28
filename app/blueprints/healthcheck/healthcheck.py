from flask import Blueprint
from blueprints.healthcheck.views.liveliness import Alive
from blueprints.healthcheck.views.readiness import Ready


blueprint = Blueprint("healthcheck", __name__)
blueprint.add_url_rule("/alive", view_func=Alive.as_view("alive"))
blueprint.add_url_rule("/ready", view_func=Ready.as_view("ready"))
