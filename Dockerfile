FROM python

RUN python -m pip install --no-cache pipenv

WORKDIR /app
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 5000

ENV MONGO_DSN=postgresql://user:password@server/ \
    GUNICORN_CMD_ARGS=""

CMD ["gunicorn", "app:create_app()"]

COPY app/ ./

RUN mkdir /logs