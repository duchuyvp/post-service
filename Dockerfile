FROM python:3.12

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /post-service

COPY pyproject.toml .
RUN python -m pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi --no-root

COPY . /post-service

CMD ["uvicorn", "post_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
