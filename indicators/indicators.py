import pandas as pd
import numpy as np

def calculate_sma(df: pd.DataFrame, window: int, column: str = 'close') -> pd.Series:
    return df[column].rolling(window=window).mean()

def calculate_rsi(df: pd.DataFrame, window: int = 14, column: str = 'close') -> pd.Series:
    delta = df[column].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=window).mean()
    avg_loss = pd.Series(loss).rolling(window=window).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    return 100 - (100 / (1 + rs))

def calculate_bollinger_bands(df: pd.DataFrame, window: int = 20, std_dev: float = 2.0, column: str = 'close'):
    sma = df[column].rolling(window=window).mean()
    std = df[column].rolling(window=window).std()
    upper_band = sma + std_dev * std
    lower_band = sma - std_dev * std
    return upper_band, lower_band

def detect_trend_zone(df: pd.DataFrame, sma_short: str = 'sma_5', sma_long: str = 'sma_20') -> pd.Series:
    return np.where(df[sma_short] > df[sma_long], 'bullish', 'bearish')
