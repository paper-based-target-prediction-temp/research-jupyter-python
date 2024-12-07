from pymongo import MongoClient
from src.core.config import settings


class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_DB_URI)
        self.db = self.client[settings.MONGO_DB_NAME]

    def get_collection(self, collection_name):
        return self.db[collection_name]


db = MongoDB()


if __name__ == "__main__":
    """ping test"""
    try:
        db.client.admin.command("ping")
        print("MongoDB 연결 성공")
    except Exception as e:
        print(f"MongoDB 연결 실패: {e}")
