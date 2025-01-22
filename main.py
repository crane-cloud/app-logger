from fastapi import FastAPI
from app.tasks import create_celery
from app import routes
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI()

    app.celery_app = create_celery()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(routes.router, prefix="/api")

    return app


app = create_app()
celery = app.celery_app
