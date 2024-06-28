from typing import Optional, List
from fastapi import HTTPException, Query, Depends
from app.database import get_collection
from app.model import Activity
from bson import json_util
from bson.objectid import ObjectId
import json
from app.helpers.paginater import paginate
from app.helpers.admin import get_current_user_id
from datetime import datetime
from pydantic import BaseModel


class ActivityQueryParams(BaseModel):
    operation: Optional[str] = None
    user_id: Optional[str] = None
    status: Optional[str] = None
    model: Optional[str] = None
    general: Optional[bool] = False
    a_project_id: Optional[str] = None
    a_cluster_id: Optional[str] = None
    a_db_id: Optional[str] = None
    a_user_id: Optional[str] = None
    a_app_id: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    page: int = Query(1, ge=1)
    per_page: int = Query(10, ge=1)

    operations: Optional[List[str]] = None
    models: Optional[List[str]] = None
    statuses: Optional[List[str]] = None
    user_ids: Optional[List[str]] = None
    project_ids: Optional[List[str]] = None


def get_activities(query_params: ActivityQueryParams, current_user_id: str = Depends(get_current_user_id)) -> dict:
    try:
        print(query_params)
        filters = {"user_id": current_user_id}
        if query_params.general:
            del filters["user_id"]
        if query_params.user_id and query_params.general:
            filters["user_id"] = query_params.user_id
        if query_params.operation:
            filters["operation"] = query_params.operation
        if query_params.status:
            filters["status"] = query_params.status
        if query_params.model:
            filters["model"] = query_params.model
        if query_params.a_project_id:
            filters["a_project_id"] = query_params.a_project_id
        if query_params.a_cluster_id:
            filters["a_cluster_id"] = query_params.a_cluster_id
        if query_params.a_db_id:
            filters["a_db_id"] = query_params.a_db_id
        if query_params.a_user_id:
            filters["a_user_id"] = query_params.a_user_id
        if query_params.a_app_id:
            filters["a_app_id"] = query_params.a_app_id
        if query_params.start:
            start_date = datetime.strptime(query_params.start, "%Y-%m-%d")
            filters.setdefault("creation_date", {}).update(
                {"$gte": start_date})
        if query_params.end:
            end_date = datetime.strptime(query_params.end, "%Y-%m-%d")
            filters.setdefault("creation_date", {}).update({"$lte": end_date})

        # multiple filters
        if query_params.operations:
            filters["operation"] = {"$in": query_params.operations}
        if query_params.models:
            filters["model"] = {"$in": query_params.models}
        if query_params.statuses:
            filters["status"] = {"$in": query_params.statuses}
        if query_params.user_ids:
            user_id_filter = {"user_id": {"$in": query_params.user_ids}}
            filters = {"$or": [user_id_filter, filters]}

        results = get_collection().find(
            filters).sort("creation_date", -1).skip(
                query_params.per_page * (query_params.page - 1)).limit(query_params.per_page)

        serialized_results = [json.loads(
            json_util.dumps(result)) for result in results]
        pagination_meta_data, paginated_items = paginate(
            serialized_results, per_page=query_params.per_page, page=query_params.page)

        return {
            "status": "success",
            "data": {
                "pagination": pagination_meta_data,
                "activity": paginated_items
            }
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
                            "message": "Internal server error"})


def get_single_activity(activity_id: str):
    try:
        activity = get_collection().find_one({"_id": ObjectId(activity_id)})
        if not activity:
            raise HTTPException(status_code=404, detail={
                                "message": "activity not found"})
        return Activity(**activity)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
                            "message": "Internal server error"})
