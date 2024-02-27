from fastapi import APIRouter, Body

import app.controllers as controllers
from app.model import Log
from fastapi import Query
from typing import Optional
from app.tasks import add_activity_task, hello


router = APIRouter()


@router.get("/")
async def index():
    hello.delay()
    return {"message": "Hello, world"}


@router.post("/logs")
def add_log(data: Log = Body(...)):
    add_activity_task.delay(data.dict())
    return {"message": "Log added successfully"}


@router.get("/logs")
async def get_logs(
        operation: Optional[str] = Query(
            None, description="Operation"),
        status: Optional[str] = Query(None, description="Status"),
        model: Optional[str] = Query(None, description="Model"),
        a_project_id: Optional[str] = Query(
            None, description="Project ID"),
        a_cluster_id: Optional[str] = Query(
            None, description="Cluster ID"),
        a_db_id: Optional[str] = Query(
            None, description="Database ID"),
        a_user_id: Optional[str] = Query(
            None, description="User ID"),
        a_app_id: Optional[str] = Query(None, description="App ID"),
        start: Optional[str] = Query(
            None, description="Start date"),
        end: Optional[str] = Query(None, description="End date")):

    return await controllers.get_logs(
        operation=operation,
        status=status,
        model=model,
        a_project_id=a_project_id,
        a_cluster_id=a_cluster_id,
        a_db_id=a_db_id,
        a_user_id=a_user_id,
        a_app_id=a_app_id,
        start=start,
        end=end)


@router.get("/logs/{log_id}", response_model=Log)
async def get_log(log_id: str) -> Log:
    return await controllers.get_log(log_id)
