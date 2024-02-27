import os
from celery import shared_task
from celery import current_app as current_celery_app
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
