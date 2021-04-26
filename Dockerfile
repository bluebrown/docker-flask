FROM python:3.8-alpine

EXPOSE 5000
CMD ["gunicorn", "app:create_app()"]
WORKDIR /app

RUN python -m pip install pipenv

COPY Pipfile ./
COPY Pipfile.lock ./

ARG pipenv_extra=""
RUN pipenv install --system --deploy --ignore-pipfile ${pipenv_extra}

ARG version="0.1.0-dev"
ARG branch="main"
ARG created="unknown"
ARG commit_hash="unknown"

LABEL org.opencontainers.created=${created} \
    org.opencontainers.url="https://github.com/bluebrown/docker-flask"  \
    org.opencontainers.source="https://github.com/bluebrown/docker-flask" \
    org.opencontainers.version=${version} \
    org.opencontainers.revision=${commit_hash} \
    org.opencontainers.vendor="rainbowstack" \
    org.opencontainers.title="flaskapp" \
    org.opencontainers.description="demo flask app" \
    org.opencontainers.documentation="https://github.com/bluebrown/docker-flask/blob/main/README.md" \
    org.opencontainers.authors="nico braun" \
    org.opencontainers.licenses="(BSD-1-Clause)" \
    org.opencontainers.ref.name=${branch} \
    org.label-schema.docker.cmd="docker run --network mongonet -p 5000:5000 flaskapp" \
    org.label-schema.docker.cmd.devel="docker run --network mongonet -p 5000:5000 \
    -e LOG_LEVEL debug -e LOG_FORMAT text -e GUNICORN_CMD_ARGS=--reload \
    -v $PWD/app:app flaskapp" \
    org.label-schema.docker.cmd.test="docker run --network mongonet flaskapp pytest -v" \
    org.label-schema.docker.cmd.debug="docker exec -ti $CONTAINER bash" \
    org.label-schema.docker.cmd.help="docker exec -ti $CONTAINER gunicorn --help" \
    org.label-schema.docker.params="LOG_LEVEL=debug|info|warning|error|critical,\
    LOG_FORMAT=json|text,\
    FILTER_PROBES=0|1 dont log requests to healthcheck endpoints with access logger,\
    GUNICORN_CMD_ARGS=see docs for all options,\
    MONGO_URI=a RFC-compliant URI" \
    dev.rainbowstack.healthcheck.readiness="GET /ready HTTP/1.1" \
    dev.rainbowstack.healthcheck.liveliness="GET /ready HTTP/1.1"

COPY README.md ./
COPY app/ ./
