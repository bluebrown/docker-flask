from flask.views import View
from flask import Response
from http import HTTPStatus


class Alive(View):
    def dispatch_request(self):
        return Response(status=HTTPStatus.OK)
