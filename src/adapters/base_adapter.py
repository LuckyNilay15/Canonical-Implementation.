from abc import ABC, abstractmethod
from typing import Dict, Any
from src.models.payment import Payment

class BaseAdapter(ABC):
    """
    The abstract interface for all client-specific adapters.
    Every new client must implement this class.
    """

    @abstractmethod
    def to_canonical(self, raw_data: Dict[str, Any]) -> Payment:
        """
        Converts client-specific raw JSON/Dict into our 
        standardized Payment object.
        """
        pass