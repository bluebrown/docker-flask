import multiprocessing
from gunicorn import glogging

# A directory to use for the worker heartbeat temporary file. Set to in memory due to docker and ebs.
worker_tmp_dir = "/dev/shm"
# bind all interfaces due to docker
bind = "0.0.0.0:5000"
# enable multi threading
worker_class = "gthread"
# recommended calculation
workers = multiprocessing.cpu_count() * 2 + 1
threads = 4

# logging
disable_redirect_access_to_syslog = True
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"

# Redirect stdout/stderr to specified file in errorlog.
capture_output = False

# make gunicorn sing json
access_log_format = '\
{"time":"%(t)s","remote_address":"%(h)s",\
"request":"%(r)s","status":%(s)s,"response_length":"%(b)s",\
"referrer":"%(f)s","user_agent":"%(a)s"}'

glogging.Logger.access_fmt = '{"access":%(message)s,"pid":%(process)d}'

glogging.Logger.error_fmt = '\
{"time":"%(created)f","name":"%(name)s","level":"%(levelname)s","message":"%(message)s","pid":%(process)d}'

glogging.Logger.syslog_fmt = glogging.Logger.error_fmt
glogging.Logger.datefmt = ""
