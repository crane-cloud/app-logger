from fastapi import APIRouter, Body, Header, HTTPException, Depends

import app.controllers as controllers
from app.model import Activity
from fastapi import Query
from typing import Optional, Annotated
from app.tasks import add_activity_task, hello
from app.helpers.auth import JWTBearer


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
# @authenticate
def get_activities(
        dependencies=Depends(JWTBearer()),
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
        end: Optional[str] = Query(None, description="End date"),
        page: int = Query(1, description="Page number", gt=0),
        per_page: int = Query(10, description="Activities per page", gt=0),
):

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
        end=end,
        page=page,
        per_page=per_page,
    )


@router.get("/activities/{activity_id}", response_model=Activity)
def get_activity(activity_id: str) -> Activity:
    return controllers.get_single_activity(activity_id)
