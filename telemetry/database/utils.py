from collections import deque

from fastapi import FastAPI


def generate_mongo_uri(host: str, port: int, user: str = None, password: str = None) -> str:
    """
    Generates a MongoDB URI.

    Parameters:
    - host (str): The hostname of the MongoDB server.
    - port (int): The port of the MongoDB server.
    - user (str): The username for MongoDB authentication (optional).
    - password (str): The password for MongoDB authentication (optional).

    Returns:
    - str: The generated MongoDB URI.
    """
    if user and password:
        uri = f"mongodb://{user}:{password}@{host}:{port}"
    else:
        uri = f"mongodb://{host}:{port}"

    return uri


async def insert_telemetry_batch(app: FastAPI, collection_name: str, queue: deque):
    if queue:
        batch = [queue.popleft() for _ in range(len(queue))]
        try:
            await app.mongodb[collection_name].insert_many(batch)
        except Exception as e:
            print("Error inserting telemetry batch:", e)
