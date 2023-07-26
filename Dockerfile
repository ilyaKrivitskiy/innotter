FROM python:3.8.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

COPY . .

RUN pip3 install poetry \
    && poetry install

