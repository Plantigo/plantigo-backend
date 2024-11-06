from app.mqtt.client import MQTTClient


def test_mqtt_connect():
    mqtt = MQTTClient("test.mosquitto.org", 1883)
    mqtt.connect()
