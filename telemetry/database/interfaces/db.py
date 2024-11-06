from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class DatabaseInterface(ABC):
    @abstractmethod
    def insert(self, collection_name: str, data: Dict[str, Any]) -> bool:
        """Inserts a document into the specified collection."""
        pass

    @abstractmethod
    def find(self, collection_name: str, query: Dict[str, Any], limit: int = 0, skip: int = 0) -> Optional[List[Dict[str, Any]]]:
        """Finds documents in the specified collection matching the query, with optional pagination."""
        pass

    @abstractmethod
    def update(self, collection_name: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> bool:
        """Updates a document in the specified collection matching the query."""
        pass

    @abstractmethod
    def delete(self, collection_name: str, query: Dict[str, Any]) -> bool:
        """Deletes a document from the specified collection matching the query."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Closes the database connection."""
        pass
