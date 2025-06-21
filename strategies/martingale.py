# strategies/martingale.py

import os
import json
from typing import Dict, Any

class SmartMartingale:
    def __init__(self, base_lot: float = 0.1, max_multiplier: int = 16, max_losses: int = 3, state_file: str = "martingale_state.json") -> None:
        self.base_lot: float = base_lot
        self.max_multiplier: int = max_multiplier
        self.max_losses: int = max_losses
        self.state_file: str = state_file
        self.state: Dict[str, Any] = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        else:
            return {"multiplier": 1, "loss_count": 0, "history": []}

    def _save_state(self) -> None:
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)

    def update_result(self, result: str) -> None:
        history = self.state["history"]
        history.append(result)

        if result == "loss":
            self.state["loss_count"] += 1
            if self.state["loss_count"] >= self.max_losses:
                print("🛑 Maksimumi i humbjeve arritur – rikthehet loti në bazë.")
                self.state["multiplier"] = 1
                self.state["loss_count"] = 0
            else:
                self.state["multiplier"] = min(self.state["multiplier"] * 2, self.max_multiplier)
        else:
            self.state["multiplier"] = 1
            self.state["loss_count"] = 0

        self.state["history"] = history[-10:]  # ruaj vetëm 10 të fundit
        self._save_state()

    def get_lot_size(self, confirmation_strength: float = 1.0) -> float:
        """
        confirmation_strength: nga 0.0 - 1.0 (p.sh. 1.0 = sinjal i fortë)
        """
        adaptive_multiplier = self.state["multiplier"] * confirmation_strength
        calculated_lot = self.base_lot * adaptive_multiplier
        return round(calculated_lot, 2)

    def get_state(self) -> Dict[str, Any]:
        return self.state
