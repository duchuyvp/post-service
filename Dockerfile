FROM python:3.12

# RUN apt install gcc libpq (no longer needed bc we use psycopg2-binary)

RUN pip install poetry

COPY pyproject.toml /pyproject.toml
COPY src/ /src/
RUN poetry install
COPY tests/ /tests/

