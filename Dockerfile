FROM python:3.8

ARG version="0.1.0-dev"
ARG vcs_url="https://github.com/bluebrown/docker-flask"
ARG vcs_branch="main"
ARG build_date="unknown"
ARG commit_hash="unknown"

EXPOSE 5000
CMD ["gunicorn", "app:create_app()"]
WORKDIR /app

ENV MONGO_DSN=postgresql://user:password@server/ \
    GUNICORN_CMD_ARGS="" \
    LOG_LEVEL=info \
    LOG_FORMAT=json \
    FILTER_PROBES='1'

RUN mkdir /logs && python -m pip install --no-cache pipenv

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv install --system --deploy --ignore-pipfile

COPY app/ ./
COPY README.md ./

LABEL org.label-schema.vendor="rainbowstack" \
    org.label-schema.name="flaskapp" \
    org.label-schema.description="demo web application" \
    org.label-schema.usage="/app/README.md" \
    org.label-schema.url=vcs_url \
    org.label-schema.vcs-url=$vcs_url \
    org.label-schema.vcs-branch=$vcs_branch \
    org.label-schema.vcs-ref=$commit_hash \
    org.label-schema.version=$version \
    org.label-schema.schema-version="1.0" \
    org.label-schema.build-date=$build_date \
    org.label-schema.docker.cmd.devel="docker run --network mongonet -p 5000:5000 flaskapp" \
    org.label-schema.docker.cmd="docker run --network mongonet -p 5000:5000 -e LOG_LEVEL debug -e LOG_FORMAT text flaskapp" \
    org.label-schema.docker.cmd.debug="docker exec -ti $CONTAINER bash" \
    org.label-schema.docker.cmd.help="docker exec -ti $CONTAINER gunicorn --help" \
    org.label-schema.docker.params="LOG_LEVEL=debug|info|warning|error|critical,\
    LOG_FORMAT=json|text,\
    FILTER_PROBES=0|1 dont log requests to healthcheck endpoints with access logger,\
    GUNICORN_CMD_ARGS=see docs for all options,\
    MONGO_DSN=valid rfc connection string"
