# live_trading/live_trader.py
import time
import pandas as pd
from models.predictor import predict_signal
from utils.order_manager import execute_trade
from features.feature_engineering import add_features

def fetch_live_price():
    url = "https://api.mexc.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=1"
    response = requests.get(url)
    data = response.json()
    close_price = float(data[0][4])
    return {
        "timestamp": pd.to_datetime(data[0][0], unit="ms"),
        "open": float(data[0][1]),
        "high": float(data[0][2]),
        "low": float(data[0][3]),
        "close": close_price,
        "volume": float(data[0][5])
    }

def run_live_trader():
    print("🚀 Live-Trader gestartet...")
    while True:
        try:
            candle = fetch_live_price()
            df = pd.DataFrame([candle])
            df = add_features(df)
            signal = predict_signal(df)
            execute_trade(signal)
        except Exception as e:
            print(f"❌ Fehler: {e}")

        time.sleep(60)

if __name__ == "__main__":
    run_live_trader()
