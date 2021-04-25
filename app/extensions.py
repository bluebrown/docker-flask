from pythonjsonlogger import jsonlogger
from logging import Filter
import json
import uuid
import json_logging


class CustomJSONLogWebFormatter(json_logging.JSONLogFormatter):
    """
    Formatter for web application log
    """

    def _format_log_object(self, record, request_util):
        json_log_object = super(CustomJSONLogWebFormatter, self)._format_log_object(
            record, request_util
        )
        if json_log_object["logger"] == "gunicorn.access":
            json_log_object["msg"] = json.loads(json_log_object["msg"])
        return json_log_object


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def process_log_record(self, log_record):
        log_record["uuid"] = uuid.uuid1()
        if log_record["name"] == "gunicorn.access":
            log_record["message"] = json.loads(log_record["message"])
        # Old Style "super" since Python 2.6's logging.Formatter is old
        return jsonlogger.JsonFormatter.process_log_record(self, log_record)


class HealthCheckFilter(Filter):
    def filter(self, record):
        msg = record.getMessage()
        return "/ready" not in msg and "/alive" not in msg
