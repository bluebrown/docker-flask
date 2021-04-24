import flask
from os import environ as env
from pymongo import MongoClient
from main import main
from healthcheck import healthcheck

app = flask.Flask(__name__)

app.config["MONGO_URI"] = env.get("MONGO_DSN")
client = MongoClient(app.config["MONGO_URI"])
app.logger.debug(client.server_info())

app.register_blueprint(main.create(client))
app.register_blueprint(healthcheck.create(client))
