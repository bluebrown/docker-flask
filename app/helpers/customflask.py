from flask import Flask, Response, jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import Aborter

_mapping = Aborter().mapping


def asJson(error):
    return {
        "code": error.code,
        "name": error.name,
        "description": error.description,
    }, error.code


class ApiResponse(Response):
    """the ApiResponse class is the default response class for the ApiFlask class.
    Its mimetype is application/json. Lists and dicts are converted to json.
    """

    charset = "utf-8"
    default_mimetype = "application/json"
    default_status = 200

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, list) or isinstance(rv, dict):
            rv = jsonify(rv)
        return super(ApiResponse, cls).force_type(rv, environ)


class ApiException(Exception):
    """The ApiException class is used by the ApiFlask class.
    When thrown it will be converted as json and send to the client."""

    def __init__(self, description, code=400, *args, **kwargs):
        self._error = _mapping[code](description, *args, **kwargs)

    def to_response(self):
        return asJson(self._error)


class ApiFlask(Flask):
    """The ApiFlask class extends Flask and turns its default behavior into
    a json api. It will also convert lists, dicts json when returned from a handler.
    Additionally it will return http errors as json."""

    response_class = ApiResponse

    def __init__(self, import_name):
        super(ApiFlask, self).__init__(import_name)
        self.register_error_handler(ApiException, self.api_error)
        self.register_error_handler(HTTPException, self.http_error)

    def api_error(self, error):
        """ "Convert api expection to http error responses."""
        self.logger.debug(error._error)
        return error.to_response()

    def http_error(self, error):
        """Return JSON instead of HTML for HTTP errors."""
        return asJson(error)
