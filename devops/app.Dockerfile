FROM python:3.12-slim

COPY pyproject.toml poetry.lock /app/

WORKDIR /app

RUN pip install poetry==2.5.1  \
    && poetry config virtualenvs.create false  \
    && poetry install --no-root

COPY src/ .