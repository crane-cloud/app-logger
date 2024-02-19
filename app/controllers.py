from typing import List
from fastapi import HTTPException

from app.database import get_log_collection
from app.model import Log
from bson import json_util
import json


async def add_log(data: dict = {}) -> bool:
    try:
        collection = await get_log_collection()
        log = Log(**data.dict())
        # print(**log.dict())
        added_item = collection.insert_one(log.dict())
        print(added_item)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
                            "message": "Internal server error"})
    return True


async def get_logs(filters: dict = None) -> List[dict]:
    try:
        collection = await get_log_collection()
        if filters:
            results = collection.find(filters)
        else:
            results = collection.find()

        serialized_results = json.loads(json_util.dumps(results))

        return serialized_results

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
                            "message": "Internal server error"})
