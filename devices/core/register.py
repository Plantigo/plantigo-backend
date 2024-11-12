from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from core.database import engine
from devices.routers import router as devices_router
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    SQLModel.metadata.create_all(engine)
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown initiated")


def register_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(devices_router)
    return app
