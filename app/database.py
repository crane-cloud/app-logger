# from motor.motor_asyncio import AsyncIOMotorClient
# import motor.motor_asyncio
from pymongo.mongo_client import MongoClient
import config

client = MongoClient(config.Base.get_mongo_uri(), port=None, connect=True)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


database = client.get_database("activity-logs")


async def get_log_collection():
    return database.get_collection("logs")
