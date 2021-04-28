from os import environ as env
from flask import Flask, g
from flask.logging import default_handler
from extensions.with_proxy_fix import with_proxy_fix

from blueprints import register_blueprints


def create_app():
    """instantiate new flask app"""
    app = Flask(__name__)
    app.logger.removeHandler(default_handler)

    app.config["MONGO_URI"] = env.get("MONGO_URI")
    app.config["PROXY_FIX"] = env.get("PROXY_FIX")

    # apply proxy fix if needed
    app = with_proxy_fix(app)

    # register all blueprints
    register_blueprints(app)

    # make sure db is closed after each request
    @app.teardown_appcontext
    def close_db(exception):
        if exception:
            app.log_exception(exception)
        if "db" in g:
            g.db.close()

    return app
