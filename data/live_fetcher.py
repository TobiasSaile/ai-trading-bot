import ccxt
import pandas as pd
import time

def fetch_eth_usdt_ohlcv(exchange_name="binance", timeframe="1h", limit=100):
    exchange = getattr(ccxt, exchange_name)()
    ohlcv = exchange.fetch_ohlcv('ETH/USDT', timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df
