from flask import Flask, Response
from pymongo.cursor import Cursor
from bson.json_util import dumps as bdumps
from werkzeug.exceptions import HTTPException
from json import dumps as jdumps


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
            rv = jdumps(rv)
        return super(ApiResponse, cls).force_type(rv, environ)


class ApiException(Exception):
    """The ApiException class is used by the ApiFlask class.
    When thrown it will be converted as json and send to the client."""

    def __init__(self, message, status=400, payload={}):
        self.message = message
        self.status = status
        self.payload = payload

    def to_dict(self):
        d = {
            "message": self.message,
            "status": self.status,
        }
        if self.payload:
            d["payload"] = self.payload
        return d


class ApiFlask(Flask):
    """The ApiFlask class extends Flask and turns its default behavior into
    a json api. It will also convert lists, dicts and pymongo cursor to json
    when returned from a handler. Additionally it will return http errors as json."""

    response_class = ApiResponse

    def __init__(self, import_name):
        super(ApiFlask, self).__init__(import_name)
        self.register_error_handler(ApiException, self.api_error)
        self.register_error_handler(HTTPException, self.http_error)

    def api_error(self, error):
        return error.to_dict(), error.status

    def http_error(self, error):
        """Return JSON instead of HTML for HTTP errors."""
        return {
            "code": error.code,
            "name": error.name,
            "description": error.description,
        }, error.code

    def make_response(self, rv):
        if isinstance(rv, tuple):
            if isinstance(rv[0], Cursor):
                rv = (bdumps(rv[0]),) + rv[1:]

        elif isinstance(rv, Cursor):
            rv = bdumps(rv)

        return Flask.make_response(self, rv)
