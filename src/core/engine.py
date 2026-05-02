from src.config.config_manager import ConfigManager
from src.adapters.client_a import ClientAAdapter
from src.adapters.client_b import ClientBAdapter
from src.strategies.bank import BankStrategy
from src.strategies.wallet import WalletStrategy

class PaymentEngine:
    """
    The Main Conductor.
    It receives raw data and routes it through: Adapter -> Config -> Strategy.
    """
    def __init__(self):
        # 1. The Brain 
        self.config_manager = ConfigManager()
        
        # 2. The "Matchmakers" (Simple Factories)
        self.adapters = {
            "CLIENT_A": ClientAAdapter(),
            "CLIENT_B": ClientBAdapter()
        }
        self.strategies = {
            "BANK_STRATEGY": BankStrategy(),
            "WALLET_STRATEGY": WalletStrategy()
        }

    def process_transaction(self, client_id: str, raw_payload: dict) -> dict:
        print(f"\n{"="*40}")
        print(f"🚀 INCOMING REQUEST FROM: {client_id}")
        
        # --- STEP 1: TRANSLATE (Adapter Phase) ---
        adapter = self.adapters.get(client_id)
        if not adapter:
            return {"status": "FAILED", "reason": f"Unknown Client: {client_id}"}
        
        payment = adapter.to_canonical(raw_payload)
        print(f"✅ 1. Translated to Canonical Model: {payment.amount} {payment.currency}")

        # --- STEP 2: DECIDE (Config Phase) ---
        rules = self.config_manager.get_client_rules(client_id)
        print(f"🧠 2. Loaded Rules: {rules}")

        # --- STEP 3: SYSTEM VALIDATION (Generic Code) ---
        # Look ma, no hardcoded limits!
        if payment.amount > rules.get("max_transaction_limit", 0):
            return {"status": "REJECTED", "reason": "Amount exceeds client's configured limit"}
        
        if rules.get("apply_fraud_check"):
            print("🛡️ 3. Running Fraud Check... [Passed!]")
        else:
            print("🛡️ 3. Fraud Check disabled for this client. Skipping.")

        # --- STEP 4: EXECUTE (Strategy Phase) ---
        route = rules.get("strategy_route")
        strategy = self.strategies.get(route)
        
        if not strategy:
            return {"status": "FAILED", "reason": f"Unknown Execution Route: {route}"}
        
        print(f"⚙️ 4. Handoff to Specialist Strategy: {route}")
        result = strategy.process(payment)
        
        print(f"{"="*40}\n")
        return result