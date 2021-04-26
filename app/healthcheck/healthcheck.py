from flask import Blueprint
from healthcheck.probes.livelyness import Alive
from healthcheck.probes.readyness import Ready


healthcheck = Blueprint("healthcheck", __name__)
healthcheck.add_url_rule("/alive", view_func=Alive.as_view("alive"))
healthcheck.add_url_rule("/ready", view_func=Ready.as_view("ready"))
