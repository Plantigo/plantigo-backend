from abc import ABC, abstractmethod
from typing import Callable

class ListenerInterface(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    def handle_message(self, topic_pattern: str, callback: Callable) -> Callable:
        pass

    @abstractmethod
    def add_topic(self, topic: str, callback: Callable[[str, str], None]):
        pass

    @abstractmethod
    def on_connect(self, client, flags, rc, properties):
        pass

    @abstractmethod
    def on_disconnect(self, client, packet, exc=None):
        pass

    @abstractmethod
    def on_message(self, client, topic, payload, qos, properties):
        pass
