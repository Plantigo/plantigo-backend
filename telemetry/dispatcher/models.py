from pydantic import BaseModel


class DeviceData(BaseModel):
    id: str
    mac_address: str
    temperature: float
    humidity: float
    pressure: float
    soil_moisture: float
    timestamp: str
