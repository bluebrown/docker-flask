from pymongo import MongoClient
from flask import current_app, _app_ctx_stack
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError


def timeoutHandler(error):
    return "", 503


def configHandler(error):
    return "", 500


class MongoController(object):
    """MongoController class is a Wrapper for a mongodb connection.
    It will take down of connection and disconnection on each request."""

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)
        app.register_error_handler(ServerSelectionTimeoutError, timeoutHandler)
        app.register_error_handler(ConfigurationError, configHandler)

    def connect(self):
        return MongoClient(current_app.config["MONGO_URI"])

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, "mongodb"):
            ctx.mongodb.close()

    @property
    def connection(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "mongodb"):
                ctx.mongodb = self.connect()
            return ctx.mongodb
