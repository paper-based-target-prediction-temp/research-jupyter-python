from motor.motor_asyncio import AsyncIOMotorClient
import logging
from src.core.config import settings


# MongoDB connection manager with Motor
class MongoDB:
    """
    MongoDB 연결 관리자
    """

    def __init__(self):
        self.client: AsyncIOMotorClient = None

    # Initialize the MongoDB connection
    async def connect(self):
        # 연결여부 확인
        if self.client:
            logging.info("MongoDB connection already exists.")
            return

        logging.info("Connecting to MongoDB...")
        try:
            # MongoDB 클라이언트 초기화
            self.client = AsyncIOMotorClient(
                str(settings.MONGO_DB_URI),
                maxPoolSize=settings.MAX_CONNECTIONS_COUNT,
                minPoolSize=settings.MIN_CONNECTIONS_COUNT,
                serverSelectionTimeoutMS=settings.SERVER_SELECTION_TIMEOUT_MS,
            )
            ping_response = await self.client.admin.command("ping")
            if int(ping_response["ok"]) != 1:
                raise Exception("Problem connecting to database cluster.")
            print(f"Ping response: {ping_response}")

            logging.info("MongoDB connection established.")
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise

    # Close the MongoDB connection
    async def close(self):
        # 연결여부 확인
        if not self.client:
            logging.warning("MongoDB connection is already closed.")
            return

        logging.info("Closing MongoDB connection...")
        self.client.close()
        self.client = None
        logging.info("MongoDB connection closed.")

    # 컨텍스트에 진입할 때 호출되어 db 연결
    async def __aenter__(self):
        await self.connect()
        return self

    # 컨텍스트에서 나갈 때 호출되어 db 연결 종료
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()


# Singleton instance for MongoDB connection
mongodb = MongoDB()


# Dependency injection for FastAPI
async def get_client() -> AsyncIOMotorClient:
    """Retrieve the MongoDB client instance."""
    if mongodb.client is None:
        await mongodb.connect()
    return mongodb.client


# get collection
async def get_collection(collection_name: str):
    client = await get_client()
    db = client[settings.MONGO_DB_NAME]
    return db[collection_name]


# 연결 확인 테스트
if __name__ == "__main__":
    import asyncio

    async def main():
        try:
            async with MongoDB() as mongo:
                await mongo.client.admin.command("ping")
                print("=== Successfully connected to MongoDB! ===")

                # 서버 상태 정보 가져오기
                server_status = await mongo.client.admin.command("serverStatus")
                current_connections = server_status["connections"]["current"]
                print(f" - Current connections: {current_connections}")

        except Exception as e:
            logging.error(f"Error during MongoDB operations: {e}")
        finally:
            await mongodb.close()
            print("=== MongoDB connection closed. ===")

    asyncio.run(main())
