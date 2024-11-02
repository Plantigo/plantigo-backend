from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Device(BaseModel):
    id: int
    name: str
    mac_address: str
    is_active: bool
    last_read: Optional[datetime]


class DeviceCreate(BaseModel):
    name: str
    mac_address: str
    is_active: Optional[bool]
