from flask.views import View
from extensions import get_db
from flask import abort, Response, current_app as app
from http import HTTPStatus


class Ready(View):
    def dispatch_request(self):
        try:
            info = get_db().server_info()
            app.logger.debug(info)
            return Response(status=HTTPStatus.OK)
        except Exception as e:
            app.logger.error(e)
            abort(HTTPStatus.SERVICE_UNAVAILABLE)
