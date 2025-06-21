from strategies.smc_strategy import SMCStrategy
from strategies.ict_strategy import ICTStrategy
from strategies.martingale import MartingaleStrategy

class CombinedStrategy:
    def __init__(self):
        self.smc = SMCStrategy()
        self.ict = ICTStrategy()
        self.martingale = MartingaleStrategy()

    def generate_signal(self, data):
        # Merr sinjal nga SMC
        smc_signal = self.smc.generate_signal(data)

        # Merr sinjal nga ICT
        ict_signal = self.ict.generate_signal(data)

        # Krahaso nëse të dy përputhen (p.sh. të dy japin 'buy' ose 'sell')
        if smc_signal and ict_signal:
            if smc_signal['type'] == ict_signal['type']:
                print("✅ Strategjitë SMC dhe ICT përputhen.")
                signal = self.martingale.generate_signal(data)
                signal['type'] = smc_signal['type']  # vendos tipin nga SMC/ICT
                return signal

        print("⚠️ Strategjitë nuk përputhen – nuk ka sinjal.")
        return None
