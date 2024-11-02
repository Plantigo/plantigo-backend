from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from devices.core.database import engine
from devices.routers.devices import router as devices_router
from dotenv import load_dotenv


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    SQLModel.metadata.create_all(engine)
    print("Application startup complete")
    yield
    print("Application shutdown initiated")


app = FastAPI(lifespan=lifespan)

app.include_router(devices_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
