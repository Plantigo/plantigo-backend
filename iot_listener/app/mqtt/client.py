import paho.mqtt.client as mqtt
from app.core.interfaces.mqtt import MQTTInterface
import logging

class MQTTClient(MQTTInterface):
    def __init__(self, broker: str, port: int, username: str, password: str):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.logger = logging.getLogger("MQTTClient")

    def connect(self):
        self.client.username_pw_set(username=self.username, password=self.password)

        self.client.connect(self.broker, self.port)
        self.logger.info(f"Connected to MQTT broker at {self.broker}:{self.port}")

    def subscribe(self, topics: list):
        for topic in topics:
            self.client.subscribe(topic)
            self.logger.info(f"Subscribed to topic: {topic}")

    def on_message(self, callback):
        self.client.on_message = callback

    def loop_forever(self):
        self.client.loop_forever()