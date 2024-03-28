from pymongo.mongo_client import MongoClient
from config import settings

mongo = MongoClient(settings.MONGO_URI, port=None, connect=True)

database_name = 'activity-logs'
if settings.FASTAPI_ENV == 'testing':
    database_name = 'testing-activity-logs'

try:
    mongo_db = mongo.get_database(database_name)
except Exception as e:
    mongo_db = mongo.get_database('testing-activity-logs')


def get_collection():
    return mongo_db["activities"]
