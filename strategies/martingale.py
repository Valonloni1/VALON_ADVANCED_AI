class MartingaleStrategy:
    def __init__(self):
        self.name = "Martingale"
        self.last_trade_loss = False
        self.base_lot = 0.1
        self.multiplier = 2
        self.current_lot = self.base_lot

    def generate_signal(self, data):
        # Simulimi i sinjalit gjithmonë Buy për testim
        print(f"📊 Martingale: Lot aktual = {self.current_lot}")

        signal = {
            "symbol": "XAUUSD",
            "type": "buy",
            "lot": self.current_lot,
            "price": data[-1]['close']
        }

        return signal

    def update_after_trade(self, profit):
        if profit < 0:
            self.last_trade_loss = True
            self.current_lot *= self.multiplier
            print(f"🔁 Humbje – rritja e lotit në {self.current_lot}")
        else:
            self.last_trade_loss = False
            self.current_lot = self.base_lot
            print("✅ Fitim – kthim në lot fillestar")
