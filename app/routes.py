from fastapi import APIRouter, Body, Header, HTTPException

import app.controllers as controllers
from app.model import Activity
from fastapi import Query
from typing import Optional, Annotated
from app.tasks import add_activity_task, hello

from app.helpers.decorators import admin_required, authenticate

router = APIRouter()


@router.get("/")
async def index():
    hello.delay()
    return {"message": "Hello, world"}


@router.post("/activities")
# @authenticate
def add_activity(data: Activity = Body(...)):
    add_activity_task.delay(data.dict())
    return {"message": "activity added successfully"}


@router.get("/activities")
@authenticate
def get_activities(
        access_token: Annotated[str | None, Header()] = None,
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

    return controllers.get_activities(
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


# unused route
@router.get("/activities/{activity_id}", response_model=Activity)
def get_activity(activity_id: str) -> Activity:
    return controllers.get_single_activity(activity_id)
