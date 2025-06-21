# risk/risk_manager.py

import MetaTrader5 as mt5
from typing import Optional

class RiskManager:
    def __init__(self, risk_percent: float = 1.0) -> None:
        self.risk_percent: float = risk_percent / 100  # p.sh. 1% = 0.01

    def get_balance(self) -> float:
        account_info = mt5.account_info()
        return account_info.balance if account_info else 0.0

    def calculate_lot_size(self, stop_loss_pips: int, symbol: str = "XAUUSD") -> float:
        balance: float = self.get_balance()
        if balance == 0:
            raise Exception("❌ Nuk mund të marr balancën nga llogaria")

        # Rreziku në para
        risk_amount: float = balance * self.risk_percent

        # Merr informata për kontratën (volumin)
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            raise Exception(f"❌ Simboli nuk u gjet: {symbol}")

        # Konvertimi i pips në çmim
        pip_value: float = 0.01 if "JPY" in symbol or symbol == "XAUUSD" else 0.0001
        sl_price_range: float = stop_loss_pips * pip_value

        tick_value: float = symbol_info.trade_tick_value
        tick_size: float = symbol_info.trade_tick_size

        if tick_value == 0 or tick_size == 0:
            raise Exception("❌ Vlerat e tick-ut janë të pavlefshme për këtë simbol")

        lot: float = risk_amount / ((sl_price_range / tick_size) * tick_value)

        lot = max(symbol_info.volume_min, min(lot, symbol_info.volume_max))
        return round(lot, 2)
