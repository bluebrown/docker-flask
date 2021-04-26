import multiprocessing
from os import environ as env

# A directory to use for the worker heartbeat temporary file. Set to in memory due to docker and ebs.
worker_tmp_dir = "/dev/shm"

# bind all interfaces due to docker
bind = "0.0.0.0:5000"

# enable multi threading
worker_class = "gthread"
workers = multiprocessing.cpu_count() * 2 + 1  # 2-4 x $(NUM_CORES)
threads = workers + 1  # 2-4 x $(NUM_CORES)

# logging
accesslog = "-"
errorlog = "/var/log/gunicorn.log"

LOG_LEVEL = env.get("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = env.get("LOG_FORMAT", "json")
FILTER_PROBES = int(env.get("FILTER_PROBES", 0))

# make gunicorn sing json

if LOG_FORMAT == "json":
    access_log_format = '{"time":"%(t)s","remote_address":"%(h)s",\
"request":"%(r)s","status":%(s)s,"response_length":"%(b)s","referrer":"%(f)s","user_agent":"%(a)s"}'

logconfig_dict = dict(
    version=1,
    disable_existing_loggers=True,
    root={"level": LOG_LEVEL, "handlers": ["stdout"]},
    loggers={
        "gunicorn.error": {
            "level": LOG_LEVEL,
            "handlers": ["stderr"],
            "propagate": False,
            "qualname": "gunicorn.error",
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["stdout"],
            "propagate": False,
            "qualname": "gunicorn.access",
        },
    },
    handlers={
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": LOG_FORMAT,
            "filters": ["healthcheck"] if FILTER_PROBES == 1 else [],
            "stream": "ext://sys.stdout",
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "formatter": LOG_FORMAT,
            "stream": "ext://sys.stderr",
        },
    },
    formatters={
        "json": {
            "()": "extensions.CustomJSONLogWebFormatter",
        },
        "text": {
            "class": "logging.Formatter",
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    filters={
        "healthcheck": {
            "()": "extensions.HealthCheckFilter",
        }
    },
)
