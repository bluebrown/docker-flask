# Flask Nginx Example

Demo flask application connected to mongodb with kubernetes compliant health probe endpoints.

## Start the app

The below command will start the flak application and a mongodb in docker container.

```console
docker-compose up
```

Once the container are running, you can post a message.

```console
$ curl -i -H "Content-Type: application/json" -X POST -d '{"message":"hello, flask"}' http://localhost:5000/msg
HTTP/1.1 201 CREATED
Server: gunicorn
Date: Sat, 24 Apr 2021 15:08:22 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 34

{"id":"60843466092d7c719ec5063b"}
```

A list of all messages can be retrieved on the root endpoint

```console
$ curl localhost:5000/
[{"_id": {"$oid": "60843466092d7c719ec5063b"}, "message": "hello, flask"}]
```

## Health Probe

As long as the app is running it will serve a 200 response on the `/alive` endpoint

```console
$ curl -I localhost:5000/alive
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 24
Server: Werkzeug/1.0.1 Python/3.9.4
Date: Fri, 23 Apr 2021 14:34:54 GMT
```

As long as the database connection is working the app will return a 200 response on `/ready`.

```console
$ curl -Is localhost:5000/ready | head -n 1
HTTP/1.0 200 OK
```

The behavior can be be tested by shutting down the database container. Once the database is down, the application with return a status 503 response.

```console
$ docker-compose stop mongodb
$ curl -Is localhost:5000/ready | head -n 1
HTTP/1.0 503 SERVICE UNAVAILABLE
```

Once the database is started up again the app will return again a 200

```console
$ docker-compose start mongodb
$ curl -Is localhost:5000/ready | head -n 1
HTTP/1.0 200 OK
```

## Environment

### Gunicorn

The `GUNICORN_CMD_ARGS` variable can be used as per [documentation](https://docs.gunicorn.org/en/20.1.0/configure.html)

```yml
GUNICORN_CMD_ARGS: "--workers=6 --threads=4 --access-logfile=/logs/access.log --log-file=/logs/error.log --log-level=DEBUG"
```

### Logging

The application logs by default into to stdout and stderr. The log format has been configured as JSON to play nicely with modern tools.

The output can also be directed to log files if needed. For this the gunicons command line args or flags can be used.

```console
docker run --network mongonet \
    -e mongodb://user:password@server/
    -e GUNICORN_CMD_ARGS="--access-logfile=/logs/access.log --log-file=/logs/error.log --log-level=DEBUG" \
    -v $PWD/logs:/logs \
    flaskapp
```

### Database DSN

The connection string is set via

```ini
MONGO_DSN=mongodb://user:password@server/
```

## Development

Install the `pre-commit hook`

```console
pre-commit install
```

Flake8 has been configured to accept a maximum line length of 119. When using VS Code, the following setting is required to make flake8 read its config from the `setup.cfg` file.

```json
"python.linting.pylintArgs": [
    "--rcfile=setup.cfg"
],
```
