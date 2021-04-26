from flask.views import View
from flask import Response


class Alive(View):
    def dispatch_request(self):
        return Response(status=200)
