from collections import deque
from datetime import datetime
from typing import Dict, Any

from database.utils import insert_telemetry_batch

telemetry_queue = deque()
BATCH_SIZE = 10


async def save_telemetry_data(payload: Dict[str, Any], args: str, kwargs: Dict[str, Any]):
    try:
        payload['mac'] = args
        payload['timestamp'] = payload.get('timestamp', int(datetime.now().timestamp() * 1000))
        telemetry_queue.append(payload)
        if len(telemetry_queue) >= BATCH_SIZE:
            await insert_telemetry_batch(kwargs.get('app'), 'telemetry', telemetry_queue)
    except Exception as e:
        print("Error saving telemetry data:", e)
