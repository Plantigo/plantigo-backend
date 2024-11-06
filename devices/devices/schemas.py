from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Device(BaseModel):
    id: UUID
    name: str
    mac_address: str
    user_id: UUID
    is_active: bool
    last_read: Optional[datetime]


class DeviceCreate(BaseModel):
    name: str
    mac_address: str
    is_active: Optional[bool]


class DeviceUpdate(BaseModel):
    name: Optional[str]
    mac_address: Optional[str]
    is_active: Optional[bool]
    last_read: Optional[datetime]
