import logging
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.settings import DEBUG, VERSION, CORS_ORIGINS
from integrations.handlers import save_telemetry_data
from integrations.listener import MQTTListener

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

mqtt_listener = MQTTListener()

def _init_app() -> FastAPI:
    logger.info("Initializing FastAPI application.")
    return FastAPI(version=VERSION, debug=DEBUG, lifespan=_lifespan)

@asynccontextmanager
async def _lifespan(app: FastAPI):
    await startup_db_client(app)
    await mqtt_listener.connect()
    register_listener(app)
    yield
    await shutdown_db_client(app)
    await mqtt_listener.disconnect()

async def startup_db_client(app):
    try:
        app.mongodb_client = AsyncIOMotorClient("mongodb://root:example@localhost:27017/")
        app.mongodb = app.mongodb_client.get_database("telemetry_db")
        logger.info("Successfully connected to MongoDB.")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")

async def shutdown_db_client(app):
    try:
        app.mongodb_client.close()
        logger.info("MongoDB connection closed.")
    except Exception as e:
        logger.error(f"Failed to close MongoDB connection: {e}")

def register_app():
    app = _init_app()
    register_router(app)
    register_middleware(app)
    logger.info("Application setup complete.")
    return app

def register_listener(app: FastAPI):
    try:
        mqtt_listener.add_topic("sensors/+/data", save_telemetry_data, app)  # Example of topic subscription
        logger.info("MQTT listener subscribed to topic: sensors/+/data.")
    except Exception as e:
        logger.error(f"Failed to subscribe MQTT listener to topic: {e}")

def register_middleware(app: FastAPI):
    try:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logger.info("CORS middleware registered.")
    except Exception as e:
        logger.error(f"Failed to register CORS middleware: {e}")

def register_router(app: FastAPI):
    logger.info("No routers registered.")
