import MetaTrader5 as mt5

class MT5Connector:
    TIMEFRAME_M15 = mt5.TIMEFRAME_M15

    def __init__(self, login, password, server):
        self.login = login
        self.password = password
        self.server = server
        self.connected = False

    def connect(self):
        if not mt5.initialize():
            print(f"❌ MT5 nuk u inicializua: {mt5.last_error()}")
            return False
        authorized = mt5.login(self.login, self.password, self.server)
        if not authorized:
            print(f"❌ Dështoi login në MT5: {mt5.last_error()}")
            return False
        self.connected = True
        print("✅ MT5 connection established")
        return True

    def get_data(self, symbol, timeframe, bars):
        if not self.connected:
            print("⚠️ Nuk ka lidhje me MT5.")
            return None
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
        if rates is None:
            print(f"⚠️ Nuk u morën të dhëna për {symbol}.")
        return rates

    def send_order(self, symbol, lot, order_type, price, sl, tp):
        print(f"🔁 Simulating order for {symbol} with lot={lot}, SL={sl}, TP={tp}")
        # Këtu duhet të shtosh kodin real për dërgimin e urdhrit në MT5

    def shutdown(self):
        mt5.shutdown()
        self.connected = False
        print("🔌 Lidhja me MT5 u mbyll.")
