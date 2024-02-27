from jsonschema import validate
import config
from typing import List, Optional
from pydantic import BaseModel
import datetime
from fastapi import FastAPI, Header, Query, HTTPException


class Log(BaseModel):
    user_id: str
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    creation_date: Optional[datetime.datetime]
    operation: str
    model: str
    status: str
    description: Optional[str] = None
    a_user_id: Optional[str] = None
    a_db_id: Optional[str] = None
    a_app_id: Optional[str] = None
    a_project_id: Optional[str] = None
    a_cluster_id: Optional[str] = None


class LogGetResponse(BaseModel):
    id: str


class LogsFilters(BaseModel):
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
