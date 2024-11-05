from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class DBDevice(SQLModel, table=True):
    __tablename__ = "devices"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    mac_address: str
    user_id: UUID
    is_active: bool = True
    last_read: Optional[datetime] = Field(default=None)
