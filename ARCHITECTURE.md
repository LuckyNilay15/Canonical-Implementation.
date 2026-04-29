# Canonical Implementation Plan

## Overview
This project demonstrates a modular architecture for handling varied client schemas using Adapter, Config, and Strategy patterns.

## 1. Directory Structure
```text
/
├── src/
│   ├── adapters/          # Normalize client schemas (Translate)
│   ├── config/            # Load client behavior (Decide)
│   ├── models/            # Canonical Domain Models (Truth)
│   ├── strategies/        # Method-specific logic (Execute)
│   ├── core/              # Orchestration Engine (Conductor)
│   └── main.py            # Entry Point
└── tests/                 # Verification logic
```

## 2. Core Concepts

### Adapter (Translate)
- Converts `ClientA_Schema` or `ClientB_Schema` into the **Canonical Model**.
- Handles key mapping (e.g., `amt` -> `amount`) and type conversions.

### Config (Decide)
- Fetches rules based on `client_id`.
- Controls flags like `enable_fraud_check` or `max_limit`.
- Dictates the `execution_route` (which strategy to use).

### Strategy (Execute)
- Interface-driven implementations for `Bank`, `Wallet`, `BNPL`, etc.
- Only cares about the normalized Canonical Model.

## 3. Detailed Phase Specifications

### Phase 1: The Canonical Model (`src/models/payment.py`)
This is your **Entity**. It defines what a "Payment" looks like inside your system, regardless of its origin.
**Fields to Implement:**
- `transaction_id`: UUID/String.
- `client_id`: To know who sent it.
- `amount`: float/Decimal (Standardized).
- `currency`: String (ISO-4217).
- `method`: Enum (BANK, WALLET, BNPL).
- `metadata`: Dict for any pass-through data.

### Phase 2: The Adapter Layer (`src/adapters/`)
The goal here is **Normalization**.
1. **BaseAdapter**: Define an interface with a `to_canonical(raw_payload: dict) -> Payment` method.
2. **ClientAAdapter**: Implement logic to map `amt` -> `amount` and set `method` to `BANK`.
3. **ClientBAdapter**: Implement logic to map `value` -> `amount` and set `method` to `WALLET`.

**Why?** Your core business logic will never see the word `amt` or `value` again. It only interacts with `Payment.amount`.

## 4. The Journey of a Request (Step-by-Step)

1.  **Ingress**: A JSON request arrives.
    - *Example (Client A)*: `{ "amt": 100, "cid": "A" }`
2.  **Identify & Adapt**:
    - Select `ClientAAdapter`.
    - Run `to_canonical()`.
    - Result: `Payment(amount=100.0, client_id='A', method='BANK')`.
3.  **Fetch Config**:
    - Lookup `client_id='A'` in your config store.
    - Result: `{ "fraud_check": true, "limit": 500, "route": "BankProcessor" }`.
4.  **Generic Validation**:
    - The Engine checks: `if payment.amount > config.limit: Error!`.
    - The Engine checks: `if config.fraud_check: run_fraud_scanner(payment)`.
5.  **Strategy Execution**:
    - Resolve strategy: `route="BankProcessor"` -> `BankStrategy`.
    - Run `strategy.process(payment)`.
## 5. Pattern Deep Dives: The "Why"

### Adapter: Decoupling from External Chaos
Clients are unreliable. They change field names, data types, and structures without warning. 
- **Theory**: By using an Adapter, you create a "Sanitized Zone". Your business logic is protected from the "Chaos" of external schemas.
- **Mental Model**: Think of it as a power adapter. Your system is a US plug (Canonical), and your clients are UK/EU/Asia outlets. The adapter makes the connection possible without changing your appliance.

### Config: Data-Driven Behavior
The biggest cause of "Spaghetti Code" is the accumulation of client-specific feature flags.
- **Theory**: Moving rules to a Config Store transitions you from "Hardcoded Logic" to "Configuration Logic".
- **Mental Model**: Your code is a **General Engine** (like a car), and the Config is the **Driver's Manual** for a specific race. The engine stays the same; the driver just changes the manual.

### Strategy: Pluggable Execution
Some logic isn't just a "flag" (on/off); it's a completely different workflow.
- **Theory**: Strategy allows you to swap out large chunks of behavior at runtime without the main Engine knowing or caring.
- **Mental Model**: Think of a delivery system. The "Order" (Canonical Model) is the same, but the "Delivery Strategy" can be by Bike, Drone, or Truck. The Warehouse (Engine) just hands the package to the "Strategy" and says "Go".

## 6. Project Philosophy
1. **Never use an `if` for a Client ID.** Use Config.
2. **Never use an `if` for a Payment Method.** Use Strategy.
3. **Always translate at the boundary.** Use Adapter.
