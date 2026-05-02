from src.strategies.base_strategy import BaseStrategy
from src.models.payment import Payment

class WalletStrategy(BaseStrategy):
    """
    The Specialist for Digital Wallet transactions.
    It focuses on fast REST API calls and security tokens.
    """

    def process(self, payment: Payment) -> dict:
        # 1. Extract the specific 'baggage' this strategy needs from metadata
        wallet_token = payment.metadata.get("token", "NO_TOKEN_PROVIDED")
        
        print(f"📱 [WALLET STRATEGY] Connecting to modern REST Wallet API...")
        print(f"   -> Processing {payment.amount} {payment.currency}")
        print(f"   -> Verifying security token: {wallet_token[:4]}...")

        if wallet_token == "NO_TOKEN_PROVIDED":
             return {
                 "status": "FAILED",
                 "provider": "WALLET_API",
                 "message": "Missing required wallet token."
             }

        # 2. Return a standardized success response
        return {
            "status": "SUCCESS",
            "provider": "WALLET_API",
            "reference_id": f"WLLT_TX_{payment.transaction_id}",
            "message": "Wallet balance successfully updated."
        }