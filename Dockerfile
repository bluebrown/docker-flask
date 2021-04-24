FROM python

RUN python -m pip install --no-cache pipenv

WORKDIR /app
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile

RUN mkdir /var/log/gunicorn

EXPOSE 5000

ENV LOG_LEVEL=INFO \
    MONGO_DSN=postgresql://user:password@server/

ENTRYPOINT [ "gunicorn" ]
CMD ["--log-level=$LOG_LEVEL", "app:app"]

COPY app/ ./
