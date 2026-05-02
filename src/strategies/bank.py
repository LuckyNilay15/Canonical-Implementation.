from src.strategies.base_strategy import BaseStrategy
from src.models.payment import Payment

class BankStrategy(BaseStrategy):
    """
    The Specialist for Bank transactions.
    It expects high-security protocols and handles legacy routing.
    """

    def process(self, payment: Payment) -> dict:
        # 1. Simulate the rigid bank logic
        print(f"🏦 [BANK STRATEGY] Initiating legacy SOAP transfer...")
        print(f"   -> Routing {payment.amount} {payment.currency} for Txn ID: {payment.transaction_id}")
        
        # 2. Pretend we are doing a complex XML request to a bank here
        simulated_bank_reference = f"BANK_REF_{payment.transaction_id[-4:]}"

        # 3. Return a standardized success response
        return {
            "status": "SUCCESS",
            "provider": "BANK_GATEWAY",
            "reference_id": simulated_bank_reference,
            "message": "Funds successfully transferred via Bank Network."
        }