from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure

from core.settings import settings


class MongoDBConnection:
    def __init__(self, mongo_uri: str, database_name: str):
        self.client = MongoClient(mongo_uri)
        self.database = self.client[database_name]
        self.is_connected = self.test_connection()

    def get_collection(self, collection_name: str) -> Collection:
        if not self.is_connected:
            raise ConnectionError("MongoDB connection not established.")
        return self.database[collection_name]

    def get_collections(self) -> list[str]:
        return self.database.list_collection_names()

    def test_connection(self) -> bool:
        try:
            self.client.admin.command("ping")
            return True
        except ConnectionFailure as e:
            return False

    def close_connection(self):
        self.client.close()


def get_collection(collection_name: str) -> Collection:
    return MongoDBConnection(settings.database_url, settings.database_name).get_collection(collection_name)
