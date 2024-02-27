from pymongo.mongo_client import MongoClient
from config import settings

mongo = MongoClient(settings.MONGO_URI, port=None, connect=True)

try:
    mongo_db = mongo.get_database("activity-logs")
except Exception as e:
    mongo_db = mongo.get_database('testing')


def get_collection():
    return mongo_db["activities"]
