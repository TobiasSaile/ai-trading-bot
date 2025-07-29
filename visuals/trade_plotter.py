import pandas as pd
import matplotlib.pyplot as plt

def plot_trading_signals(df, trades):
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['close'], label='Close Price', linewidth=2)

    buy_signals = [(t['timestamp'], t['price']) for t in trades if t['action'] == 'BUY']
    sell_signals = [(t['timestamp'], t['price']) for t in trades if t['action'] == 'SELL']

    if buy_signals:
        buy_x, buy_y = zip(*buy_signals)
        plt.scatter(buy_x, buy_y, marker='^', color='green', label='BUY', s=100)

    if sell_signals:
        sell_x, sell_y = zip(*sell_signals)
        plt.scatter(sell_x, sell_y, marker='v', color='red', label='SELL', s=100)

    plt.title('Trading Chart with Buy/Sell Signals')
    plt.xlabel('Timestamp')
    plt.ylabel('Price (USDT)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Beispielnutzung (nach dem Trading)
# df = ...
# trades = ...
plot_trading_signals(df, trades)
