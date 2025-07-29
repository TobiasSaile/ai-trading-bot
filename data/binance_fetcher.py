# data/binance_fetcher.py
from binance.client import Client
from config.binance_keys import API_KEY, API_SECRET
import pandas as pd
import time

client = Client(API_KEY, API_SECRET)

def fetch_eth_usdt_ohlcv(interval="1h", limit=500):
    klines = client.get_klines(symbol="ETHUSDT", interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "_", "_", "_", "_", "_", "_"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    return df[["timestamp", "open", "high", "low", "close", "volume"]]
