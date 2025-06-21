from connector.mt5_connector import MT5Connector
from strategies.ict_smc import CombinedStrategy
from risk.risk_manager import RiskManager
from config import LOGIN, PASSWORD, SERVER
import time

if __name__ == "__main__":
    print("🚀 Nisja e robotit VALON_ADVANCED_AI...")

    # 1️⃣ Lidhja me MT5
    mt5 = MT5Connector(LOGIN, PASSWORD, SERVER)
    mt5.connect()

    # 2️⃣ Inicializimi i strategjisë dhe risk managerit
    strategy = CombinedStrategy()
    risk = RiskManager()

    # 3️⃣ Loop tregtar
    try:
        while True:
            data = mt5.get_data("XAUUSD", timeframe=mt5.TIMEFRAME_M15, bars=50)
            signal = strategy.generate_signal(data)

            if signal:
                lot = risk.calculate_lot(balance=1000, risk_percent=1.5, stop_loss_pips=50)
                signal['lot'] = lot
                mt5.send_order(
                    symbol=signal['symbol'],
                    lot=signal['lot'],
                    order_type=signal['type'],
                    price=signal['price'],
                    sl=0,
                    tp=0
                )

            time.sleep(60)
    except KeyboardInterrupt:
        print("🛑 Ndaluar me sukses nga përdoruesi.")
    finally:
        mt5.shutdown()
