from flask.views import View
from flask import send_file


class IndexPage(View):
    def dispatch_request(self):
        return send_file("main/static/index.html")
