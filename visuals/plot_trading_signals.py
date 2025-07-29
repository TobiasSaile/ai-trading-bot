import matplotlib.pyplot as plt

def plot_signals_and_equity(df, trades):
    equity_curve = df['close'].pct_change().fillna(0).cumsum() * 100 + 10_000

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

    ax1.plot(df['timestamp'], df['close'], label='Close Price', linewidth=2)
    buy_signals = [(t['timestamp'], t['price']) for t in trades if t['action'] == 'BUY']
    sell_signals = [(t['timestamp'], t['price']) for t in trades if t['action'] == 'SELL']

    if buy_signals:
        buy_x, buy_y = zip(*buy_signals)
        ax1.scatter(buy_x, buy_y, marker='^', color='green', label='BUY', s=100)

    if sell_signals:
        sell_x, sell_y = zip(*sell_signals)
        ax1.scatter(sell_x, sell_y, marker='v', color='red', label='SELL', s=100)

    ax1.set_title('📈 ETH/USDT Preis + Signale')
    ax1.set_ylabel('Preis (USDT)')
    ax1.legend()
    ax1.grid(True)

    ax2.plot(df['timestamp'], equity_curve, color='blue', label='Equity Curve')
    ax2.set_title('🏦 Portfolio-Wert (simuliert)')
    ax2.set_ylabel('Equity (USDT)')
    ax2.set_xlabel('Zeit')
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.show()
