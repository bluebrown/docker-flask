from flask import g, current_app
from pymongo import MongoClient


def get_db():
    if "db" not in g:
        g.db = MongoClient(current_app.config["MONGO_URI"])
    return g.db
