from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Dict, Any, Optional

class PaymentMethod(Enum):
    BANK = "BANK"
    WALLET = "WALLET"
    BNPL = "BNPL"

class PaymentStatus(Enum):
    CREATED = "CREATED"
    VALIDATING = "VALIDATING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

@dataclass
class Payment:
    transaction_id: str
    client_id: str
    amount: Decimal
    currency: str
    method: PaymentMethod
    status: PaymentStatus = PaymentStatus.CREATED
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """
        Logic that runs right after the object is created.
        We ensure the currency is always uppercase for consistency.
        """
        self.currency = self.currency.upper()



