from os import environ as env
from flask import Flask
from flask.logging import default_handler
from werkzeug.middleware.proxy_fix import ProxyFix
from pymongo import MongoClient
from main import main
from healthcheck import healthcheck


def create_app():
    """ instantiate new flask app """
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)
    app.logger.removeHandler(default_handler)

    app.config["MONGO_URI"] = env.get("MONGO_DSN")
    client = MongoClient(app.config["MONGO_URI"])

    app.register_blueprint(main.create(client))
    app.register_blueprint(healthcheck.create(client))

    return app
