import json
import os
from typing import Dict, Any

class ConfigManager:
    """
    Loads 'Behavior as Data' from the settings file.
    In a production system, this would query a Database or Redis.
    """
    
    def __init__(self, config_path: str = "src/config/settings.json"):
        self.config_path = config_path
        self._cache: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        # We load the JSON once to keep it fast
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as file:
                self._cache = json.load(file)
        else:
            print("Warning: Config file not found!")

    def get_client_rules(self, client_id: str) -> Dict[str, Any]:
        """
        Returns the specific rules for a client.
        Provides safe defaults if the client doesn't exist.
        """
        default_rules = {
            "apply_fraud_check": True,  # Safe default
            "max_transaction_limit": 0.0,  # Prevent transactions if unknown
            "strategy_route": "UNKNOWN"
        }
        return self._cache.get(client_id, default_rules)