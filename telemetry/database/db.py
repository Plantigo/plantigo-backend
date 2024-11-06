import logging
from typing import Dict, Any, Optional, List, Union
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from core.settings import MONGO_URI, MONGO_DB_NAME
from database.interfaces.db import DatabaseInterface

logger = logging.getLogger(__name__)


class MongoDBService(DatabaseInterface):
    def __init__(self, uri: Optional[str] = None, db_name: Optional[str] = None):
        self.uri = uri or MONGO_URI
        self.db_name = db_name or MONGO_DB_NAME

        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]

    def insert(self, collection_name: str, data: Dict[str, Any]) -> bool:
        try:
            self.db[collection_name].insert_one(data)
            logger.info(f"Inserted data into {collection_name}: {data}")
            return True
        except PyMongoError as e:
            logger.error(f"Failed to insert data into {collection_name}: {e}")
            return False

    def find(self, collection_name: str, query: Dict[str, Any], limit: int = 0, skip: int = 0) -> Optional[
        List[Dict[str, Any]]]:
        try:
            results = self.db[collection_name].find(query).skip(skip).limit(limit)
            data = list(results)
            logger.info(f"Found {len(data)} documents in {collection_name} matching {query}")
            return data
        except PyMongoError as e:
            logger.error(f"Failed to find data in {collection_name}: {e}")
            return None

    def update(self, collection_name: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> bool:
        try:
            result = self.db[collection_name].update_one(query, {'$set': update_data})
            if result.modified_count > 0:
                logger.info(f"Updated document in {collection_name} matching {query} with {update_data}")
                return True
            else:
                logger.warning(f"No document matched for update in {collection_name} with {query}")
                return False
        except PyMongoError as e:
            logger.error(f"Failed to update data in {collection_name}: {e}")
            return False

    def delete(self, collection_name: str, query: Dict[str, Any]) -> bool:
        try:
            result = self.db[collection_name].delete_one(query)
            if result.deleted_count > 0:
                logger.info(f"Deleted document in {collection_name} matching {query}")
                return True
            else:
                logger.warning(f"No document matched for deletion in {collection_name} with {query}")
                return False
        except PyMongoError as e:
            logger.error(f"Failed to delete data from {collection_name}: {e}")
            return False

    def close(self):
        self.client.close()
        logger.info("Closed MongoDB connection.")
