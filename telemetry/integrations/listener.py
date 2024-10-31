import inspect
import json
import logging
import re
from typing import Callable, Dict

from gmqtt import Client as MQTTClient

from core.settings import MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_IT
from integrations.interfaces.listener import ListenerInterface

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MQTTListener(ListenerInterface):
    def __init__(self, client_id: str | None = None, host: str | None = None,
                 port: int | None = None,
                 username: str | None = None,
                 password: str | None = None):
        self.client = MQTTClient(client_id or MQTT_CLIENT_IT, logger=logger)
        self.client.set_config({'reconnect_retries': 10, 'reconnect_delay': 60})

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.host = host or MQTT_HOST
        self.port = port or MQTT_PORT
        self.username = username or MQTT_USERNAME
        self.password = password or MQTT_PASSWORD
        self.topic_callbacks: Dict[str, Callable[[str, str], None]] = {}

    async def connect(self):
        logger.info("Starting MQTT connection...")
        try:
            if self.username and self.password:
                self.client.set_auth_credentials(self.username, self.password)
            await self.client.connect(self.host, self.port, keepalive=120)
            logger.info(f"Connected to MQTT broker at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")

    async def disconnect(self):
        logger.info("Disconnecting from MQTT broker...")
        await self.client.disconnect()
        logger.info("Disconnected from MQTT broker.")

    def handle_message(self, topic_pattern: str, callback: Callable) -> Callable:
        def wrapper(actual_topic: str, payload: str):
            pattern = topic_pattern.replace("+", r"([^/]+)")
            wildcard_match = re.match(pattern, actual_topic)
            args = wildcard_match.group(1) if wildcard_match and wildcard_match.groups() else None
            logger.debug(f"Processing message from topic {actual_topic} with details {details}")

            try:
                if not payload.strip():
                    logger.warning(f"Received empty payload on topic {actual_topic}")
                    return
                try:
                    data = json.loads(payload)
                except json.JSONDecodeError:
                    data = payload

                callback_signature = inspect.signature(callback)
                if "imei" in callback_signature.parameters and "details" in callback_signature.parameters and args:
                    callback(data, args)
                else:
                    callback(data)
            except Exception as e:
                logger.error(f"Error processing message on topic {actual_topic}: {e}")

        return wrapper

    def add_topic(self, topic: str, callback: Callable[[str, str], None]):
        logger.info(f"Subscribing to topic: {topic}")
        try:
            wrapped_callback = self.handle_message(topic, callback)
            self.topic_callbacks[topic] = wrapped_callback
            self.client.subscribe(topic)
            logger.info(f"Successfully subscribed to topic: {topic}")
        except Exception as e:
            logger.error(f"Failed to subscribe to topic {topic}: {e}")

    def on_connect(self, client, flags, rc, properties):
        logger.info("Successfully connected to MQTT broker.")
        for topic in self.topic_callbacks:
            self.client.subscribe(topic)
            logger.info(f"Re-subscribed to topic: {topic}")

    def on_disconnect(self, client, packet, exc=None):
        if exc:
            logger.warning(f"Unexpected disconnection from MQTT broker: {exc}")
        else:
            logger.info("Disconnected from MQTT broker.")

    def on_message(self, client, topic, payload, qos, properties):
        logger.debug(f"Received message on topic {topic}: {payload.decode('utf-8')}")
        matched_callback = None
        for topic_pattern, callback in self.topic_callbacks.items():
            pattern = topic_pattern.replace("+", r"([^/]+)").replace("#", r"(.*)")
            if re.fullmatch(pattern, topic):
                matched_callback = callback
                break

        if matched_callback:
            try:
                matched_callback(topic, payload.decode("utf-8"))
            except Exception as e:
                logger.error(f"Error processing message on topic {topic}: {e}")
        else:
            logger.warning(f"No callback registered for topic: {topic}")
