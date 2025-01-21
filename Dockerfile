FROM python:3.10

WORKDIR /app

ENV DEBIAN_FRONTEND='noninteractive'

RUN apt-get update && apt install -y curl

RUN pip install poetry

ENV PATH="${PATH}:/root/.local/bin"

COPY ./pyproject.toml /app/pyproject.toml

COPY ./poetry.lock /app/poetry.lock


RUN poetry install --no-root

COPY . /app

#for celery to have a different working directory
COPY . /celery-app

EXPOSE 8000

ENTRYPOINT ["sh", "/app/scripts/start.sh"]

