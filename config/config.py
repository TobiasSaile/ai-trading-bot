# config/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# MEXC API Keys (live + testnet möglich, nie im Code hardcoden!)
MEXC_API_KEY = os.getenv("MEXC_API_KEY")
MEXC_SECRET_KEY = os.getenv("MEXC_SECRET_KEY")

# Trading-Konfiguration
SYMBOL = "BTCUSDT"
TRADE_QUANTITY_USDT = 50  # pro Trade einsetzen

# Trading-Modus: 'LIVE' oder 'PAPER'
TRADING_MODE = os.getenv("TRADING_MODE", "PAPER")
