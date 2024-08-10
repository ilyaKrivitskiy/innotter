FROM python:3.8.10-buster

#SHELL ["/bin/bash", "-c"]
WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

COPY poetry.lock pyproject.toml /app/

COPY . /app

RUN apt-get update && \
    pip3 install --upgrade pip && \
    pip3 install poetry && \
    poetry install --no-dev --no-interaction --no-ansi&& \
    poetry config virtualenvs.create false

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
