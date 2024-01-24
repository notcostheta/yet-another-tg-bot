from sys import exit as exiter

from motor.motor_asyncio import AsyncIOMotorClient

from bot.configs.config import MONGO_URI, SESSION_NAME
from bot.utils.logging import LOGGER


class MongoDb:
    def __init__(self, collection):
        self.collection = collection

    async def read_document(self, document_id):
        try:
            return await self.collection.find_one({"_id": document_id})
        except Exception as e:
            LOGGER(__name__).error(f"Error reading document: {e}")
            return None

    async def update_document(self, document_id, updated_data):
        try:
            updated_data = {"$set": updated_data}
            await self.collection.update_one(
                {"_id": document_id}, updated_data, upsert=True
            )
        except Exception as e:
            LOGGER(__name__).error(f"Error updating document: {e}")

    async def delete_document(self, document_id):
        try:
            await self.collection.delete_one({"_id": document_id})
        except Exception as e:
            LOGGER(__name__).error(f"Error deleting document: {e}")

    async def total_documents(self):
        try:
            return await self.collection.count_documents({})
        except Exception as e:
            LOGGER(__name__).error(f"Error counting documents: {e}")
            return 0

    async def get_all_id(self):
        try:
            return await self.collection.distinct("_id")
        except Exception as e:
            LOGGER(__name__).error(f"Error getting document IDs: {e}")
            return []


async def check_mongo_uri(MONGO_URI: str) -> None:
    try:
        mongo = AsyncIOMotorClient(MONGO_URI)
        await mongo.server_info()
    except:
        LOGGER(__name__).error(
            "Error in Establishing connection with MongoDb URI. Please enter valid uri in the config section."
        )
        raise Exception("Invalid MongoDB URI")


mongodb = AsyncIOMotorClient(MONGO_URI)

database = mongodb.SESSION_NAME

users = MongoDb(database.users)
chats = MongoDb(database.chats)
songs = MongoDb(database.songs)
albums = MongoDb(database.albums)
