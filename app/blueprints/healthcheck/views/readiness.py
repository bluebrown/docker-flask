from flask.views import View
from global_objects import db
from flask import current_app


class Ready(View):
    """The Ready class implements the readiness endpoint"""

    def dispatch_request(self):
        info = db.connection.server_info()
        current_app.logger.debug(info)
        return ""
