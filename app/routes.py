from fastapi import APIRouter, Body

import app.controllers as controllers
from app.model import Log, LogGetResponse


router = APIRouter()


@router.post("/logs")
async def add_log(data: Log = Body(...)):
    return await controllers.add_log(data)


@router.get("/logs")
async def get_logs(filters: dict = None):
    return await controllers.get_logs(filters)
