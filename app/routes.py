from datetime import datetime
from app.database import get_collection
from fastapi import APIRouter, Body, Depends, Query

import app.controllers as controllers
from app.model import Activity
from typing import Optional
from app.tasks import add_activity_task, hello

# from app.helpers.decorators import admin_required, authenticate
from app.helpers.auth import JWTBearer
from app.helpers.admin import get_current_user_id

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
        general: Optional[bool] = Query(
            False, description="Get any user activities"),
        user_id: Optional[str] = Query(None, description="User ID"),
        #    Multiple fields
        operations: Optional[list[str]] = Query(
            None, description="List of operations"),
        models: Optional[list[str]] = Query(
            None, description="List of models"),
        statuses: Optional[list[str]] = Query(
            None, description="List of statuses"),
        user_ids: Optional[list[str]] = Query(
            None, description="List of user IDs"),
        a_tag_ids: Optional[list[str]] = Query(
            None, description="List of tag IDs"),

):
    params = {
        "operation": operation,
        "status": status,
        "model": model,
        "a_project_id": a_project_id,
        "a_cluster_id": a_cluster_id,
        "a_db_id": a_db_id,
        "a_user_id": a_user_id,
        "a_app_id": a_app_id,
        "start": start,
        "end": end,
        "page": page,
        "per_page": per_page,
        "user_id": user_id,
        "general": general,
        # Multiple
        "operations": operations,
        "models": models,
        "statuses": statuses,
        "user_ids": user_ids,
        "a_tag_ids": a_tag_ids,
    }
    current_user_id = get_current_user_id(dependencies)
    return controllers.get_activities(
        controllers.ActivityQueryParams(**params), current_user_id=current_user_id
    )


# unused route
@router.get("/activities/{activity_id}", response_model=Activity)
def get_activity(activity_id: str) -> Activity:
    return controllers.get_single_activity(activity_id)
