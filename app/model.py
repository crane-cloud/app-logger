from typing import Optional
from pydantic import BaseModel
import datetime
from fastapi import Query
from pydantic import BaseModel, EmailStr


class Activity(BaseModel):
    user_id: str
    user_email: Optional[EmailStr] = None
    user_name: Optional[str] = None
    creation_date: Optional[datetime.datetime.date]
    operation: str
    model: str
    status: str
    description: Optional[str] = None
    a_user_id: Optional[str] = None
    a_db_id: Optional[str] = None
    a_app_id: Optional[str] = None
    a_project_id: Optional[str] = None
    a_cluster_id: Optional[str] = None


class ActivityGetResponse(BaseModel):
    id: str


class ActivitiesFilters(BaseModel):
    operation: Optional[str] = Query(None, description="Operation")
    status: Optional[str] = Query(None, description="Status")
    model: Optional[str] = Query(None, description="Model")
    a_project_id: Optional[str] = Query(None, description="Project ID")
    a_cluster_id: Optional[str] = Query(None, description="Cluster ID")
    a_db_id: Optional[str] = Query(None, description="Database ID")
    a_user_id: Optional[str] = Query(None, description="User ID")
    a_app_id: Optional[str] = Query(None, description="App ID")
    start: Optional[str] = Query(None, description="Start date", format="date")
    end: Optional[str] = Query(None, description="End date", format="date")
