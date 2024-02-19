from typing import Union

from fastapi import FastAPI
from app.controllers import router

app = FastAPI()

app.include_router(router, prefix="/api")
