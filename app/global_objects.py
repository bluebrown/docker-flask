""" This file exists to avoid circular imports while using the object in the blueprints """

from extensions.flask_pymongo import MongoController

db = MongoController()
