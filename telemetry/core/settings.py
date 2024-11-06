import os
from pathlib import Path

from database.utils import generate_mongo_uri

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

VERSION = os.getenv('VERSION', '0.1.0')

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:8081").split(",")
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "test")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "test")
MQTT_CLIENT_IT = os.getenv("MQTT_CLIENT_ID", "telemetry-api")

LOG_LEVEL = os.getenv("LOG_LEVEL", "debug")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", 8000))

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "example")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "telemetry_db")
MONGO_URI = generate_mongo_uri(MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASSWORD)
MONGO_MAX_CONNECTIONS = int(os.getenv("MONGO_MAX_CONNECTIONS", 10))
