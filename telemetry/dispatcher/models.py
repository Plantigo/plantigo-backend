from typing import Dict, Any

from pydantic import BaseModel


class DeviceBaseModel(BaseModel):
    id: str
    mac_address: str
    temperature: float
    humidity: float
    pressure: float
    soil_moisture: float
    timestamp: str

    @classmethod
    def from_dict(cls, data):
        try:
            return cls(
                id=str(data.get("_id", "")),
                mac_address=data.get("mac_address", ""),
                temperature=float(data.get("temperature", 0.0) or 0.0),
                humidity=float(data.get("humidity", 0.0) or 0.0),
                pressure=float(data.get("pressure", 0.0) or 0.0),
                soil_moisture=float(data.get("soil_moisture", 0.0) or 0.0),
                timestamp=str(data.get("timestamp", ""))
            )
        except (TypeError, ValueError) as e:
            raise ValueError(f"Error converting data to DeviceData: {e}") from e
