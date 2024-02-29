from datetime import datetime
from app.database import get_collection
from celery import shared_task
from celery import current_app as current_celery_app
from fastapi import HTTPException
from app.model import Activity
from config import settings


def create_celery():
    celery_app = current_celery_app
    # prefixed with CELERY_
    celery_app.config_from_object(settings, namespace="CELERY")

    return celery_app


@shared_task
def hello():
    print('hello')
    return 'hello'


@shared_task
def add_activity_task(data: dict = {}) -> bool:
    try:
        activity = Activity(**data)
        activity.creation_date = datetime.now().isoformat()
        added_data = get_collection().insert_one(activity.dict())
        return added_data.acknowledged
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
                            "message": "Internal server error"})
