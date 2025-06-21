import pandas as pd

class SMCStrategy:
    def __init__(self):
        self.name = "SMC"

    def generate_signal(self, data):
        df = pd.DataFrame(data)

        if df.empty or len(df) < 5:
            print("📉 Të dhënat janë të pamjaftueshme për analizë SMC.")
            return None

        # Shembull shumë i thjeshtë i një logjike SMC:
        latest = df.iloc[-1]
        prev = df.iloc[-2]

        bos_up = latest['close'] > prev['high']
        bos_down = latest['close'] < prev['low']

        if bos_up:
            print("🔼 SMC sinjal për Buy")
            return {
                "symbol": "XAUUSD",
                "type": "buy",
                "price": latest['close']
            }

        elif bos_down:
            print("🔽 SMC sinjal për Sell")
            return {
                "symbol": "XAUUSD",
                "type": "sell",
                "price": latest['close']
            }

        return None
