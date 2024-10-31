from pydantic import BaseModel

class DeviceData(BaseModel):
    mac_address: str
    sensor1: float
    sensor2: float
    sensor3: float
    sensor4: float
    timestamp: float