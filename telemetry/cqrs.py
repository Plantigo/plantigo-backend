import json
from models import DeviceData
from typing import Dict, List

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            return {mac: [DeviceData(**entry) for entry in entries] for mac, entries in data.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump({mac: [entry.dict() for entry in entries] for mac, entries in data.items()}, file, indent=4)

data_store: Dict[str, List[DeviceData]] = load_data()

def save_device_data(data: DeviceData):
    if data.mac_address not in data_store:
        data_store[data.mac_address] = []
    data_store[data.mac_address].append(data)
    save_data(data_store)  #

# Odczyt (Query)
def get_device_data(mac_address: str):
    if mac_address in data_store and data_store[mac_address]:
        return data_store[mac_address][-1]
    else:
        return {"error": "No data found for this device"}