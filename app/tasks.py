import os
from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
celery_app = Celery(__name__,
                    broker=redis_url,
                    backend=redis_url,
                    include=['app.tasks'])


@celery_app.task
def hello():
    print('hello')
    return 'hello'
