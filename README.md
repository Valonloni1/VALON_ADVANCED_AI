![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/build-passing-brightgreen)

# VALON_ADVANCED_AI

🤖 **VALON_ADVANCED_AI** është një robot tregtar i avancuar për Forex, i ndërtuar në Python, që kombinon strategji të fuqishme si ICT, SMC, Martingale, Trailing Stop dhe AI Risk Management me lidhje të plotë për MetaTrader 5 (MT5).

---

## 🔥 Karakteristikat kryesore

- 📊 **Strategji Inteligjente**: ICT + SMC (BOS, OB, FVG)
- ⚙️ **Menaxhim Risku**: Lot size automatik bazuar në balancë dhe rrezik të paracaktuar
- ♻️ **Strategji Martingale e përmirësuar**: Me kontroll të mençur për rrezik
- 🎯 **Trailing Stop Dinamik**: I përshtatur sipas lëvizjeve të tregut
- 🧠 **Modul AI**: Për optimizim të performancës tregtare
- 🧾 **Mbështetje për instrumente të njohura**: XAUUSD, EURUSD, GBPUSD, USDJPY, etj.

---

## 🧩 Strukturë e projektit

```plaintext
VALON_ADVANCED_AI/
│
├── main.py                   # Nisja e robotit
├── config.py                 # Parametrat kryesorë të sistemit
├── requirements.txt          # Libraritë e nevojshme
│
├── connector/
│   └── mt5_connector.py      # Lidhja me llogarinë MT5
│
├── strategies/
│   ├── ict_strategy.py       # Strategjia ICT
│   ├── smc_strategy.py       # Strategjia SMC
│   ├── martingale.py         # Strategjia Martingale
│   └── ict_smc.py            # Kombinim i strategjive ICT + SMC
│
├── risk/
│   └── risk_manager.py       # Llogaritja e madhësisë së lotit dhe kufizimet
│
├── ai/
│   └── ai_module.py          # Logjika për AI/optimizim
│
└── tools/
    └── utils.py              # Funksione ndihmëse
