# utils/exchange_client.py
import ccxt
import os
from dotenv import load_dotenv

load_dotenv()
exchange = ccxt.mexc({
    'apiKey': os.getenv("MEXC_API_KEY"),
    'secret': os.getenv("MEXC_SECRET"),
    'enableRateLimit': True
})
ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='1m', limit=100)
exchange.create_market_buy_order('BTC/USDT', amount_in_btc)
exchange.create_market_sell_order('BTC/USDT', amount_in_btc)
mode = "live"  # oder "paper"
if mode == "live":
    exchange.create_market_buy_order(...)
else:
    print("🧪 Paper Trade: BUY", ...)