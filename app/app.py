from os import environ as env
from flask import Flask
from flask.logging import default_handler
from werkzeug.middleware.proxy_fix import ProxyFix
from main.main import main
from healthcheck.healthcheck import healthcheck
import re


def create_app():
    """instantiate new flask app"""
    app = Flask(__name__)
    app.logger.removeHandler(default_handler)

    proxy_fix = env.get("PROXY_FIX")
    if proxy_fix:
        kwargs = {
            k: int(v.strip('"')) for k, v in re.findall(r'(\S+)=(".*?"|\S+)', proxy_fix)
        }
        app.logger.debug(f"parsed PROXY_FIX: {kwargs}")
        app.wsgi_app = ProxyFix(app.wsgi_app, **kwargs)

    app.config["MONGO_URI"] = env.get("MONGO_URI")

    app.register_blueprint(main)
    app.register_blueprint(healthcheck)

    return app
