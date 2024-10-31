import logging
from contextlib import asynccontextmanager

from core.settings import DEBUG, VERSION, CORS_ORIGINS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from integrations.handlers import save_telemetry_data
from integrations.listener import MQTTListener

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

mqtt_listener = MQTTListener()


def _init_app() -> FastAPI:
    return FastAPI(version=VERSION, debug=DEBUG, lifespan=lifespan)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mqtt_listener.connect()
    register_listener()
    yield
    await mqtt_listener.disconnect()


def register_app():
    app = _init_app()
    register_router(app)
    register_middleware(app)

    return app


def register_listener():
    mqtt_listener.add_topic("sensors/+/data", save_telemetry_data)  # Example of topic subscription


def register_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_router(app: FastAPI):
    pass
