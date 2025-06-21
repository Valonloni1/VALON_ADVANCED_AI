from connector.mt5_connector import MT5Connector
from strategies.smc_strategy import SMCStrategy
from risk.risk_manager import RiskManager

def main():
    print("🚀 Nisja e robotit VALON_ADVANCED_AI...")

    # 1️⃣ Lidhja me MT5
    connector = MT5Connector()
    if not connector.connect():
        print("❌ Dështoi lidhja me MT5.")
        return

    print("✅ Lidhja me MT5 u realizua me sukses.")

    # 2️⃣ Ngarko strategjinë
    strategy = SMCStrategy()

    # 3️⃣ Ngarko risk manager
    risk_manager = RiskManager()

    # 4️⃣ Merr të dhënat dhe ekzekuto strategjinë
    data = connector.get_market_data("XAUUSD", timeframe="M15", count=200)

    if data is not None:
        signal = strategy.generate_signal(data)

        if signal:
            lot_size, sl, tp = risk_manager.calculate_position(signal)
            connector.execute_trade(signal, lot_size, sl, tp)
        else:
            print("📉 Asnjë sinjal i vlefshëm për tregti.")
    else:
        print("⚠️ Nuk u morën të dhëna nga MT5.")

    # 5️⃣ Shkëput lidhjen
    connector.shutdown()

if __name__ == "__main__":
    main()
