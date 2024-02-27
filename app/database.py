from pymongo.mongo_client import MongoClient
from config import settings

# client = MongoClient(settings.MONGO_URI, port=None, connect=True)

# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


# async def get_log_collection():
#     return database.get_collection("activities")


mongo = MongoClient(settings.MONGO_URI, port=None, connect=True)

try:
    # mongo_db = mongo.get_default_database()
    mongo_db = mongo.get_database("activity-activities")
except Exception as e:
    mongo_db = mongo.get_database('testing')

database = mongo.get_database("activity-activities")


def get_collection():
    return mongo_db["activities"]


async def get_log_collection():
    return database.get_collection("activities")
