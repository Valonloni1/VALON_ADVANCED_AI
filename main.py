# main.py

from connector.mt5_connector import MT5Connector
from strategies.smc_strategy import SMCStrategy
from risk.risk_manager import RiskManager
from tools.utils import log_message

def main():
    log_message("🚀 Nisja e robotit VALON_ADVANCED_AI...")

    # 1. Lidhja me MetaTrader 5
    mt5 = MT5Connector()
    if not mt5.connect():
        log_message("❌ Dështoi lidhja me MT5", level="error")
        return

    # 2. Inicializimi i strategjisë
    strategy = SMCStrategy(symbol="XAUUSD", timeframe="M15")

    # 3. Inicializimi i risk manager-it
    risk_manager = RiskManager(capital=1000, risk_per_trade=1.5)

    # 4. Marrja e të dhënave historike
    candles = mt5.get_candles("XAUUSD", "M15", 100)
    if not candles:
        log_message("❌ Nuk u morën të dhënat historike.", level="error")
        return

    # 5. Analiza e strategjisë
    signal = strategy.check_signal(candles)

    # 6. Kontrolli i sinjalit
    if signal:
        lot_size, sl_points = risk_manager.calculate_risk(candles)
        log_message(f"✅ Sinjal gati për tregti: {signal}, lot size: {lot_size}, SL: {sl_points}")

        if mt5.can_trade():
            mt5.execute_trade(symbol="XAUUSD", signal=signal, lot_size=lot_size, sl_points=sl_points)
        else:
            log_message("⚠️ Llogaria nuk është gati për tregti.", level="warning")
    else:
        log_message("ℹ️ Asnjë sinjal tregtie për momentin.")

    # 7. Mbyllja e sesionit
    mt5.shutdown()
    log_message("🧠 Roboti përfundoi sesionin.")

if __name__ == "__main__":
    main()
