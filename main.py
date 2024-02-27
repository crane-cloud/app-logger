from fastapi import FastAPI

from app import routes

app = FastAPI()

app.include_router(routes.router, prefix="/api")
