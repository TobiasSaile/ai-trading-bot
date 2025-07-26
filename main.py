# main.py
import ccxt
import pandas as pd

def fetch_ohlcv(symbol='BTC/USDT', timeframe='1h', limit=500):
    exchange = ccxt.mexc()
    data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

if __name__ == "__main__":
    df = fetch_ohlcv()
    df.to_csv("data/btcusdt_1h.csv", index=False)
    print("📁 Daten gespeichert unter: data/btcusdt_1h.csv")

# In einer separaten Datei, z.B. main.py

import pandas as pd
from paper_trading.paper_trader import PaperTrader

# Daten laden
df = pd.read_csv("data/btcusdt_1h.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Paper-Trader starten
trader = PaperTrader()
logs, final_value = trader.run(df, short_window=5, long_window=15)


print("\n".join(logs))
print(f"Endwert: {final_value:.2f} USDT")