from config import SYMBOL, TIMEFRAME

class ICTStrategy:
    def __init__(self, symbol: str = SYMBOL, timeframe: str = TIMEFRAME, ema_period: int = 50):
        self.symbol = symbol
        self.timeframe = timeframe
        self.ema_period = ema_period

    def generate_signal(self, data):
        if data is None or len(data) < self.ema_period:

            print("⚠️ Të dhënat janë të pamjaftueshme për ICT analizë.")
            return None

        closes = [c['close'] for c in data]
        ema = sum(closes[-self.ema_period:]) / self.ema_period

        last_close = closes[-1]

        if last_close > ema:
            print("🔼 ICT sinjal për Buy")
            return {"symbol": self.symbol, "type": "buy", "price": last_close}
        elif last_close < ema:
            print("🔽 ICT sinjal për Sell")
            return {"symbol": self.symbol, "type": "sell", "price": last_close}

        return None
