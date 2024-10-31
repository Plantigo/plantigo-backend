import datetime
import json
import paho.mqtt.client as mqtt
from models import DeviceData
from cqrs import save_device_data
from config import MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD
from typing import Callable, Dict


class MQTTListener:
    def __init__(self, broker=MQTT_BROKER, port=MQTT_PORT, username=MQTT_USERNAME, password=MQTT_PASSWORD):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        self.broker = broker
        self.port = port
        self.username = username
        self.password = password

    def connect(self):
        try:
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)
            self.client.connect(self.broker, self.port)
            self.client.subscribe("sensors/+/data")
            self.client.loop_start()
            logger.info("Connecting to MQTT broker at %s:%d", self.broker, self.port)
        except Exception as e:
            logger.error("Failed to connect to MQTT broker: %s", e)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Successfully connected to MQTT broker.")
        else:
            logger.warning("Failed to connect to MQTT broker, return code %d", rc)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning("Unexpectedly disconnected from MQTT broker.")
        else:
            logger.info("Disconnected from MQTT broker.")

    def on_message(self, client, userdata, message):
        topic_parts = message.topic.split("/")
        mac_address = topic_parts[1]
        payload = message.payload.decode("utf-8")
        logger.info("Received message from %s: %s", mac_address, payload)

        try:
            data = DeviceData(mac_address=mac_address,timestamp=datetime.datetime.now().timestamp(), **json.loads(payload))
            save_device_data(data)
        except Exception as e:
            logger.error("Error processing message from %s: %s", mac_address, e)