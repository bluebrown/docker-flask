import multiprocessing

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
errorlog = "/logs/app.log"

# make gunicorn sing json
access_log_format = '\
{"time":"%(t)s","remote_address":"%(h)s",\
"request":"%(r)s","status":%(s)s,"response_length":"%(b)s",\
"referrer":"%(f)s","user_agent":"%(a)s"}'

logconfig_dict = dict(
    version=1,
    disable_existing_loggers=True,
    root={"level": "DEBUG", "handlers": ["json"]},
    loggers={
        "gunicorn.error": {
            "level": "DEBUG",
            "handlers": ["error_json"],
            "propagate": False,
            "qualname": "gunicorn.error",
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["json"],
            "propagate": False,
            "qualname": "gunicorn.access",
        },
    },
    handlers={
        "json": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "filters": ["healthcheck"],
            "stream": "ext://sys.stdout",
        },
        "error_json": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stderr",
        },
    },
    formatters={
        "json": {
            "()": "extensions.CustomJSONLogWebFormatter",
        },
    },
    filters={
        "healthcheck": {
            "()": "extensions.HealthCheckFilter",
        }
    },
)
