from gunicorn.glogging import Logger as GLogger
import logging
import json_logging
from os import environ as env
import sys


class CustomLogger(GLogger):
    def setup(self, cfg):
        super(CustomLogger, self).setup(cfg)
        handler = logging.StreamHandler(sys)
        handler.setFormatter(json_logging.BaseJSONFormatter)
        self._set_handler(handler)


class VoidLogger(GLogger):
    def setup(self, cfg):
        LOG_LEVEL = logging.getLevelName(env.get("LOGLEVEL", "INFO").upper())
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)
        self.error_log.setLevel(LOG_LEVEL)
        self.access_log.setLevel(LOG_LEVEL)
