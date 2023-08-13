#!/bin/bash -x

poetry run python3 ./src/manage.py migrate --noinput
poetry run python3 ./src/manage.py runserver 0.0.0.0:8080

exec "$@"