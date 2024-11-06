import logging

from app.core.interfaces.db import DatabaseInterface


class TelemetryHandler:
    def __init__(self, db: DatabaseInterface):
        self.db = db
        self.logger = logging.getLogger("TelemetryHandler")

    def handle_message(self, topic: str, payload: dict):
        try:
            self.logger.info(f"Processing message from {topic}: {payload}")
            self.db.save({"topic": topic, "payload": payload})
            self.logger.info("Message saved successfully")
        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
