from typing import List
from fastapi import HTTPException

from app.database import get_log_collection
from app.model import Log, LogsFilters
from bson import json_util
import json
import datetime


async def add_log(data: dict = {}) -> bool:
    try:
        collection = await get_log_collection()
        log = Log(**data.dict())
        # print(**log.dict())
        log.creation_date = datetime.datetime.now().date()
        added_item = collection.insert_one(log.dict())
        print(added_item)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
                            "message": "Internal server error"})
    return True


async def get_logs(operation: str, status: str, model: str,
                   a_project_id: str, a_cluster_id: str, a_db_id: str, a_user_id: str,
                   a_app_id: str, start: str, end: str) -> List[dict]:
    try:
        collection = await get_log_collection()

        results = collection.find()

        serialized_results = json.loads(json_util.dumps(results))

        return serialized_results

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
                            "message": "Internal server error"})
