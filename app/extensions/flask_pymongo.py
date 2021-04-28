from pymongo import MongoClient
from flask import current_app, _app_ctx_stack


class MongoController(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

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
