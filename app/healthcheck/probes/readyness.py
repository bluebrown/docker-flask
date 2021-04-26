from flask.views import View
from extensions import get_db
from flask import abort, Response, current_app as app


class Ready(View):
    def dispatch_request(self):
        try:
            info = get_db().server_info()
            app.logger.debug(info)
            return Response(status=200)
        except Exception as e:
            app.logger.error(e)
            abort(503)
