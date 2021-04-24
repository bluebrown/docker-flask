FROM python

RUN python -m pip install --no-cache pipenv

WORKDIR /app
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile

RUN mkdir /var/log/gunicorn

EXPOSE 5000

ENV LOG_LEVEL=ERROR \
    ACCESS_LOG_LEVEL=INFO \
    MONGO_DSN=postgresql://user:password@server/database \
    GUNICORN_WORKER_CLASS=gthread  \
    GUNICORN_WORKERS=2 \
    GUNICORN_THREADS=4 

ENTRYPOINT ./entrypoint.sh

COPY app/ ./
COPY entrypoint.sh ./
