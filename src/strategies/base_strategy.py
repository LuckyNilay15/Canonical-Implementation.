from abc import ABC, abstractmethod
from src.models.payment import Payment

class BaseStrategy(ABC):
    """
    The abstract interface for all execution strategies.
    Whether it's a Bank, Wallet, or Crypto, they all must 
    implement the `process` method.
    """

    @abstractmethod
    def process(self, payment: Payment) -> dict:
        """
        Executes the business logic using the standardized 
        Canonical Payment object.
        """
        pass