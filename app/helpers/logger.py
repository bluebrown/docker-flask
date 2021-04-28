from logging import Filter
import json
import json_logging


class CustomJSONLogWebFormatter(json_logging.JSONLogFormatter):
    """Formatter for web application log"""

    def _format_log_object(self, record, request_util):
        json_log_object = super(CustomJSONLogWebFormatter, self)._format_log_object(
            record, request_util
        )
        if json_log_object["logger"] == "gunicorn.access":
            json_log_object["msg"] = json.loads(json_log_object["msg"])
        return json_log_object


class HealthCheckFilter(Filter):
    """Filter Healthcheck endpoints to keep access logs slim"""

    def filter(self, record):
        msg = record.getMessage()
        return "/ready" not in msg and "/alive" not in msg
