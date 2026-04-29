from decimal import Decimal
from typing import Dict, Any
from src.adapters.base_adapter import BaseAdapter
from src.models.payment import Payment, PaymentMethod

class ClientBAdapter(BaseAdapter):
    """
    Adapter for Client B (Wallet).
    Maps: 
    - id            -> transaction_id
    - value (cents) -> amount (dollars)
    - currency_code -> currency
    """

    def to_canonical(self, raw_data: Dict[str, Any]) -> Payment:
        # Intuition: Conversion from cents to dollars
        raw_amount = Decimal(str(raw_data.get("value", 0)))
        normalized_amount = raw_amount / Decimal("100")

        return Payment(
            transaction_id=str(raw_data.get("id")),
            client_id="CLIENT_B",
            amount=normalized_amount,
            currency=raw_data.get("currency_code", "USD"),
            method=PaymentMethod.WALLET,
            metadata={
                "wallet_id": raw_data.get("wallet_id"),
                "token": raw_data.get("token")
            }
        )
