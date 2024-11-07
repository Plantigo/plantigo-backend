import os

from app.db.utils import generate_mongo_uri


class Config:
    MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
    MQTT_USERNAME = os.getenv("MQTT_USERNAME", 'test')
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", 'test')
    MQTT_TOPICS = os.getenv("MQTT_TOPICS", "sensors/+/data").split(",")
    MONGODB_HOST = os.getenv("MONGO_HOST", "94.72.104.160")
    MONGODB_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGODB_USER = os.getenv("MONGO_USER", "root")
    MONGODB_PASSWORD = os.getenv("MONGO_PASSWORD", "KrTmS483hNRCvKjMjXVx")
    MONGODB_DB_NAME = os.getenv("MONGO_DB_NAME", "telemetry_db")
    MONGODB_URI = generate_mongo_uri(MONGODB_HOST, MONGODB_PORT, MONGODB_USER, MONGODB_PASSWORD)
    MONGODB_MAX_CONNECTIONS = int(os.getenv("MONGO_MAX_CONNECTIONS", 10))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
