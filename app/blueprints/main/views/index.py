from flask.views import View
from flask import send_file


class IndexPage(View):
    """The IndexPage class implements an endpoint to serve a
    index.html page from the static dir."""

    def dispatch_request(self):
        return send_file("blueprints/main/static/index.html")
