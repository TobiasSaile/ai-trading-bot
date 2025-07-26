import pandas as pd
import os
from glob import glob

def load_latest_log():
    files = sorted(glob("logs/session_*.csv"))
    if not files:
        print("❌ Keine Log-Dateien gefunden.")
        return None
    return pd.read_csv(files[-1], parse_dates=["timestamp"])

def analyze_log(df):
    trades = df[df['action'].isin(['close', 'reverse'])].copy()
    entries = df[df['action'].isin(['entry', 'reverse'])].copy()

    if trades.empty or entries.empty:
        print("⚠️ Nicht genug Daten zum Auswerten.")
        return

    trades.reset_index(drop=True, inplace=True)
    entries.reset_index(drop=True, inplace=True)

    # Nur Paare aus entry & close
    trades['entry_price'] = entries['price']
    trades['pnl'] = (trades['price'] - trades['entry_price']) * trades['position']
    trades['duration'] = (trades['timestamp'] - entries['timestamp']).dt.total_seconds() / 3600

    total_return = trades['pnl'].sum()
    win_trades = trades[trades['pnl'] > 0]
    loss_trades = trades[trades['pnl'] < 0]
    winrate = len(win_trades) / len(trades) * 100
    avg_win = win_trades['pnl'].mean() if not win_trades.empty else 0
    avg_loss = loss_trades['pnl'].mean() if not loss_trades.empty else 0
    sharpe = trades['pnl'].mean() / trades['pnl'].std() * (len(trades) ** 0.5) if trades['pnl'].std() else 0

    equity = trades['pnl'].cumsum()
    max_dd = (equity.cummax() - equity).max()

    print("\n📊 PERFORMANCE TRACKER")
    print(f"Anzahl Trades:           {len(trades)}")
    print(f"Gewinntrades:           {len(win_trades)}")
    print(f"Verlusttrades:          {len(loss_trades)}")
    print(f"Winrate:                {winrate:.2f} %")
    print(f"Ø Gewinn:               {avg_win:.2f}")
    print(f"Ø Verlust:              {avg_loss:.2f}")
    print(f"Gesamtertrag (PnL):     {total_return:.2f}")
    print(f"Max. Drawdown:          {max_dd:.2f}")
    print(f"Sharpe Ratio (≈):       {sharpe:.2f}")

if __name__ == "__main__":
    df = load_latest_log()
    if df is not None:
        analyze_log(df)
