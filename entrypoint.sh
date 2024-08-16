#!/bin/bash -x

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

poetry run python3 ./src/manage.py migrate --noinput
poetry run python3 ./src/manage.py runserver 0.0.0.0:8080

exec "$@"