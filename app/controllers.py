from typing import List
from fastapi import HTTPException
from app.database import get_collection
from app.model import Activity
from bson import json_util
from bson.objectid import ObjectId
import json

from datetime import datetime


def get_activities(operation: str, status: str, model: str,
                         a_project_id: str, a_cluster_id: str, a_db_id: str, a_user_id: str,
                         a_app_id: str, start: str, end: str) -> List[dict]:
    try:
        filters = {}
        all_filters = []
        if a_project_id:
            all_filters.append({"project_id": a_project_id})
        if a_cluster_id:
            all_filters.append({"cluster_id": a_cluster_id})
        if a_db_id:
            all_filters.append({"db_id": a_db_id})
        if a_user_id:
            all_filters.append({"user_id": a_user_id})
        if a_app_id:
            all_filters.append({"app_id": a_app_id})
        if status:
            all_filters.append({"status": status})
        if operation:
            all_filters.append({"operation": operation})
        if model:
            all_filters.append({"model": model})

        if start:
            all_filters.append({
                "creation_date": {
                    "$gte": datetime.strptime(start, "%Y-%m-%d")
                }
            })
        if end:
            all_filters.append({
                "creation_date": {
                    "$lte": datetime.strptime(end, "%Y-%m-%d")
                }
            })

        if all_filters:
            filters["$and"] = all_filters

        results = get_collection().find(filters)

        serialized_results = json.loads(json_util.dumps(results))

        return serialized_results

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
