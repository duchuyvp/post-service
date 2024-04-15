FROM python:3.12

# RUN apt install gcc libpq (no longer needed bc we use psycopg2-binary)

WORKDIR /post-service

RUN pip install poetry

COPY pyproject.toml /pyproject.toml
RUN poetry install

COPY . .
