from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    @abstractmethod
    def save(self, data: dict):
        pass

    @abstractmethod
    def find(self, query: dict):
        pass

    @abstractmethod
    def update(self, query: dict, data: dict):
        pass

    @abstractmethod
    def delete(self, query: dict):
        pass
