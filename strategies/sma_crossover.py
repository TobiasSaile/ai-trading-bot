# strategies/sma_crossover.py
import pandas as pd

def sma_strategy(df, short_window=10, long_window=20):
    df = df.copy()
    df['sma_short'] = df['close'].rolling(window=short_window).mean()
    df['sma_long'] = df['close'].rolling(window=long_window).mean()

    df['position'] = 0
    df.loc[df['sma_short'] > df['sma_long'], 'position'] = 1
    df.loc[df['sma_short'] < df['sma_long'], 'position'] = -1

    return df
