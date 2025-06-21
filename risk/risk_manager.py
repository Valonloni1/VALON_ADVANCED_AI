# risk/risk_manager.py

class RiskManager:
    def __init__(self, capital=1000, risk_percent=1.5):
        self.capital = capital
        self.risk_percent = risk_percent  # risk për trade në përqindje

    def calculate_lot(self, balance=None, risk_percent=None, stop_loss_pips=50, pip_value=0.1):
        if balance is None:
            balance = self.capital
        if risk_percent is None:
            risk_percent = self.risk_percent

        risk_amount = balance * (risk_percent / 100)
        lot_size = risk_amount / (stop_loss_pips * pip_value)
        return round(lot_size, 2)
