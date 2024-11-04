from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class DBDevice(SQLModel, table=True):
    __tablename__ = "devices"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    mac_address: str
    user_id: str
    is_active: bool = True
    last_read: Optional[datetime] = Field(default=None)
