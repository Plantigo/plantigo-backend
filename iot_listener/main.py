import logging

from app.config import Config
from app.core.handlers.telemetry_handler import TelemetryHandler
from app.db.mongodb import MongoDB
from app.mqtt.client import MQTTClient

logging.basicConfig(level=Config.LOG_LEVEL)

db = MongoDB(Config.MONGODB_URI, Config.MONGODB_DB_NAME)
mqtt_client = MQTTClient(Config.MQTT_BROKER, Config.MQTT_PORT, Config.MQTT_USERNAME, Config.MQTT_PASSWORD)
handler = TelemetryHandler(db)


def message_callback(client, userdata, message):
    payload = message.payload.decode()
    handler.handle_message(message.topic, payload)


mqtt_client.connect()
mqtt_client.subscribe(Config.MQTT_TOPICS)
mqtt_client.on_message(message_callback)
mqtt_client.loop_forever()
