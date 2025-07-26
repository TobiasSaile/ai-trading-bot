import pandas as pd
import matplotlib.pyplot as plt
from strategies.sma_crossover import sma_strategy

def simulate_equity(df, short, long):
    df = sma_strategy(df.copy(), short, long)
    df['returns'] = df['close'].pct_change()
    df['strategy'] = df['position'].shift(1) * df['returns']
    return df['strategy'].cumsum()

def plot_top_strategies(df, configs, top_n=3):
    plt.figure(figsize=(12, 6))
    
    for i in range(top_n):
        short = int(configs.iloc[i]['short_window'])
        long = int(configs.iloc[i]['long_window'])
        equity = simulate_equity(df, short, long)
        label = f"SMA {short}/{long}"
        plt.plot(df['timestamp'], equity, label=label)
    
    # Buy & Hold Vergleich
    df['returns'] = df['close'].pct_change()
    buy_hold = df['returns'].cumsum()
    plt.plot(df['timestamp'], buy_hold, label='Buy & Hold', linestyle='--', color='gray')

    plt.title("Top SMA-Strategien – Kumulierte Performance")
    plt.xlabel("Zeit")
    plt.ylabel("Kumulierte Rendite")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Daten einlesen
    df = pd.read_csv("data/btcusdt_1h.csv", parse_dates=['timestamp'])
    configs = pd.read_csv("data/sma_grid_results.csv").sort_values(by='return', ascending=False)

    plot_top_strategies(df, configs, top_n=3)
