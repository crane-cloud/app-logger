import os


class Base:
    @staticmethod
    def get_mongo_uri():
        MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        # print(MONGO_URI)
        return MONGO_URI
