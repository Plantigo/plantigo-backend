from typing import Dict, Any

from core.register import register_app
from fastapi import Query

app = register_app()


def serialize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    if "_id" in document:
        document["_id"] = str(document["_id"])
    return document


@app.get("/")
async def get_telemetry_by_mac(mac: str = Query(...)):
    cursor = app.mongodb["telemetry"].find({"mac": mac})
    result = await cursor.to_list(length=100)
    return [serialize_document(doc) for doc in result]
