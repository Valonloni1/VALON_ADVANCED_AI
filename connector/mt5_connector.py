# connector/mt5_connector.py

import MetaTrader5 as mt5

class MT5Connector:
    def __init__(self, login, password, server):
        self.login = login
        self.password = password
        self.server = server

    def connect(self):
        if not mt5.initialize(login=self.login, password=self.password, server=self.server):
            raise Exception(f"❌ MT5 connection failed: {mt5.last_error()}")
        print("✅ MT5 connection established")

    def shutdown(self):
        mt5.shutdown()
        print("🔌 MT5 connection closed")

    def get_data(self, symbol, timeframe, bars):
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
        if rates is None:
            raise Exception(f"⚠️ Failed to get data for {symbol}")
        return rates

    def send_order(self, symbol, lot, order_type, price, sl, tp):
        print(f"🔁 Simulating order for {symbol} with lot={lot}, SL={sl}, TP={tp}")
