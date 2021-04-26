FROM python:3.8

EXPOSE 5000
CMD ["gunicorn", "app:create_app()"]
WORKDIR /app

RUN python -m pip install pipenv

COPY Pipfile ./
COPY Pipfile.lock ./

ARG pipenv_extra=""
RUN pipenv install --system --deploy --ignore-pipfile ${pipenv_extra}

ARG version="0.1.0-dev"
ARG vcs_url="https://github.com/bluebrown/docker-flask"
ARG vcs_branch="main"
ARG build_date="unknown"
ARG commit_hash="unknown"

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
    MONGO_DSN=valid rfc connection string"

COPY README.md ./
COPY app/ ./
