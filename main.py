from fastapi import FastAPI
from app.tasks import celery_app

from app import routes

app = FastAPI()

app.include_router(routes.router, prefix="/api")

celery = celery_app