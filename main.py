from fastapi import FastAPI
from app.tasks import create_celery
from app import routes


def create_app() -> FastAPI:
    app = FastAPI()

    app.celery_app = create_celery()

    app.include_router(routes.router, prefix="/api")

    return app


app = create_app()
celery = app.celery_app

