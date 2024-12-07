from pymongo import MongoClient
from src.core.config import settings


class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_DB_URI)
        self.db = self.client[settings.MONGO_DB_NAME]

    def get_collection(self, collection_name):
        return self.db[collection_name]


db = MongoDB()
