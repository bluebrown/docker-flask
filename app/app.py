from os import environ as env
from flask.logging import default_handler

from helpers.customflask import ApiFlask
from helpers.with_proxy_fix import with_proxy_fix
from blueprints import register_blueprints
from global_objects import db


app = ApiFlask(__name__)
app.logger.removeHandler(default_handler)
app.config["MONGO_URI"] = env.get("MONGO_URI")
app.config["PROXY_FIX"] = env.get("PROXY_FIX")
app = with_proxy_fix(app)
db.init_app(app)
register_blueprints(app)
