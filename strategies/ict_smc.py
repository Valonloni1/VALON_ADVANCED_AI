# strategies/ict_smc.py

from strategies.smc_strategy import SMCStrategy
from strategies.ict_strategy import ICTStrategy
from config import DEFAULT_SYMBOL
from typing import Optional

class CombinedICTSMCStrategy:
    def __init__(self, symbol: str = DEFAULT_SYMBOL) -> None:
        self.symbol: str = symbol
        self.smc: SMCStrategy = SMCStrategy(symbol=symbol)
        self.ict: ICTStrategy = ICTStrategy(symbol=symbol)

    def generate_signal(self) -> Optional[str]:
        smc_signal: Optional[str] = self.smc.generate_signal()
        ict_signal: Optional[str] = self.ict.generate_signal()

        trend_confirms: bool = self._trend_agreement(smc_signal, ict_signal)
        both_agree: bool = smc_signal == ict_signal and smc_signal is not None

        if both_agree and trend_confirms:
            print(f"✅ KONFIRMIM I FUQISHËM: {smc_signal}")
            return smc_signal
        elif both_agree:
            print("⚠️ Sinjalet përputhen por trendi nuk konfirmon.")
        elif smc_signal or ict_signal:
            print("🟡 Sinjal i pjesshëm (vetëm njëra strategji është aktive).")
        else:
            print("ℹ️ Pa sinjal të vlefshëm.")
        return None

    def _trend_agreement(self, smc_signal: Optional[str], ict_signal: Optional[str]) -> bool:
        if smc_signal == "BUY" and ict_signal == "BUY":
            return True
        elif smc_signal == "SELL" and ict_signal == "SELL":
            return True
        else:
            return False
