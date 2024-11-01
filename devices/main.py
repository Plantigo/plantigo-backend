from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    print("Application startup complete")
    yield
    print("Application shutdown initiated")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
