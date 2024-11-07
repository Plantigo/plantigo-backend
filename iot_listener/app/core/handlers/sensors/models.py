from dataclasses import dataclass, asdict
import datetime
import json
from typing import Any

@dataclass
class TelemetryData:
    mac_address: str
    temperature: int
    humidity: int
    pressure: int
    soil_moisture: int
    timestamp: str

    @classmethod
    def from_payload(cls, mac_address: str, payload: str):
        try:
            data = json.loads(payload)
            required_keys = ["sensor1", "sensor2", "sensor3", "sensor4"]
            if not all(key in data for key in required_keys):
                raise KeyError(f"Missing keys in payload: {payload}")

            return cls(
                mac_address=mac_address,
                temperature=data["sensor1"],
                humidity=data["sensor2"],
                pressure=data["sensor3"],
                soil_moisture=data["sensor4"],
                timestamp=datetime.datetime.utcnow().isoformat(),
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON payload: {payload}") from e
        except KeyError as e:
            raise ValueError(f"Missing required key in payload: {e}") from e
