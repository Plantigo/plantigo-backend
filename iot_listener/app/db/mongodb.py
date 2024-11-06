from pymongo import MongoClient
from app.core.interfaces.db import DatabaseInterface

class MongoDB(DatabaseInterface):
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def save(self, data: dict):
        return self.db.telemetry.insert_one(data)

    def find(self, query: dict):
        return self.db.telemetry.find(query)

    def update(self, query: dict, data: dict):
        return self.db.telemetry.update_one(query, {"$set": data})

    def delete(self, query: dict):
        return self.db.telemetry.delete_one(query)