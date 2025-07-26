import pandas as pd
import ta
from ta.trend import SMAIndicator
import os

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['sma_5'] = ta.trend.sma_indicator(df['close'], window=5)
    df['sma_10'] = SMAIndicator(close=df['close'], window=10).sma_indicator()
    df['sma_15'] = ta.trend.sma_indicator(df['close'], window=15)
    df['return'] = df['close'].pct_change()
    df['rsi_14'] = ta.momentum.rsi(df['close'], window=14)
    bb = ta.volatility.BollingerBands(close=df['close'], window=20, window_dev=2)
    df['bb_middle'] = bb.bollinger_mavg()
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    df['bb_width'] = df['bb_upper'] - df['bb_lower']
    df['macd'] = ta.trend.macd(df['close'])
    df['momentum'] = ta.momentum.roc(df['close'], window=5)
    # Target nur für Training
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
    df.dropna(inplace=True)
    return df

def main():
    input_path = "data/btcusdt_1h.csv"
    output_path = "data/features.csv"
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Daten nicht gefunden: {input_path}")
    df = pd.read_csv(input_path, parse_dates=["timestamp"])
    df = add_features(df)
    print("Features für das Modell:", df.columns.tolist())  # Debug
    df.to_csv(output_path, index=False)
    print(f"✅ Features gespeichert unter: {output_path}")

if __name__ == "__main__":
    main()
