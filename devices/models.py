from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Device(SQLModel, table=True):
    __tablename__ = "devices"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    mac_address: str
    is_active: bool = True
    last_read: Optional[datetime] = Field(default=None)
