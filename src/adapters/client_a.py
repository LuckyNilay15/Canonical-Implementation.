from decimal import Decimal
from typing import Dict, Any
from src.adapters.base_adapter import BaseAdapter
from src.models.payment import Payment, PaymentMethod

class ClientAAdapter(BaseAdapter):
    """
    Adapter for Client A (Bank).
    Maps: 
    - txn_id -> transaction_id
    - amt    -> amount
    - cur    -> currency
    """

    def to_canonical(self, raw_data: Dict[str, Any]) -> Payment:
        return Payment(
            transaction_id=str(raw_data.get("txn_id")),
            client_id="CLIENT_A",
            amount=Decimal(str(raw_data.get("amt", "0.00"))),
            currency=raw_data.get("cur", "USD"),
            method=PaymentMethod.BANK,
            metadata={
                "original_txn_id": raw_data.get("txn_id")
            }
        )