FROM python:3.10

WORKDIR /app

ENV DEBIAN_FRONTEND='noninteractive'

RUN apt-get update && apt install -y curl

COPY ./README.md /app/README.md

RUN pip install poetry

ENV PATH="${PATH}:/root/.local/bin"

COPY . /app

RUN poetry install


#for celery to have a different working directory
COPY . /celery-app

EXPOSE 8000

ENTRYPOINT ["sh", "/app/scripts/start.sh"]

