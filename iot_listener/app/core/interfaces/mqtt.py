from abc import ABC, abstractmethod

class MQTTInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def subscribe(self, topics: list):
        pass

    @abstractmethod
    def on_message(self, callback):
        pass

    @abstractmethod
    def loop_forever(self):
        pass
