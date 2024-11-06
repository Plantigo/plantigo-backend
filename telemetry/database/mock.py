from typing import Dict, Any

from database.interfaces.db import DatabaseInterface


class MongoDBService(DatabaseInterface):
    def update(self, collection_name: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> bool:
        pass

    def delete(self, collection_name: str, query: Dict[str, Any]) -> bool:
        pass

    def close(self) -> None:
        pass

    def insert(self, collection_name: str, data: dict):
        print(f"Inserting into {collection_name}: {data}")
        return True

    def find(self, collection_name: str, query: dict):
        print(f"Finding in {collection_name} with query: {query}")
