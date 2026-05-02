from src.core.engine import PaymentEngine

def main():
    print("Starting Payment Service...")
    engine = PaymentEngine()

    # --- 1. Client A (The Legacy Bank) ---
    # They send weird field names and amounts in dollars.
    client_a_payload = {
        "txn_id": "A-998877",
        "amt": "20000",
        "cur": "USD"
    }

    # --- 2. Client B (The Modern Wallet) ---
    # They send different field names, and amounts in CENTS!
    client_b_payload = {
        "id": "WLLT-554433",
        "value": 15000,           # This is $150.00
        "currency_code": "USD",
        "wallet_id": "USER_XYZ_123",
        "token": "SECURE_REST_TOKEN_99"
    }

    # Run Client A
    result_a = engine.process_transaction("CLIENT_A", client_a_payload)
    print("Final Output A:", result_a)

    # Run Client B
    result_b = engine.process_transaction("CLIENT_B", client_b_payload)
    print("Final Output B:", result_b)

if __name__ == "__main__":
    main()