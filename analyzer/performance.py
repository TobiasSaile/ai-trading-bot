import pandas as pd
import json
import os


def analyze_trades(log_df: pd.DataFrame, output_dir="data"):
    trades = []
    entry_price = None
    entry_time = None
    direction = None
    equity_start = None

    for idx, row in log_df.iterrows():
        if "ENTRY" in row["action"]:
            entry_price = row["price"]
            entry_time = row["timestamp"]
            direction = "long"
            equity_start = row["equity"]
        elif "REVERSE" in row["action"] and entry_price is not None:
            exit_price = row["price"]
            exit_time = row["timestamp"]
            equity_end = row["equity"]
            pnl = equity_end - equity_start

            trades.append({
                "entry_time": entry_time,
                "exit_time": exit_time,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "pnl": pnl,
                "equity_start": equity_start,
                "equity_end": equity_end,
                "direction": direction
            })

            # Prepare for next trade
            entry_price = exit_price
            entry_time = exit_time
            equity_start = equity_end

    trades_df = pd.DataFrame(trades)
    if trades_df.empty:
        print("❌ Keine Trades zum Analysieren gefunden.")
        return

    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    trade_log_path = os.path.join(output_dir, "trade_log.csv")
    trades_df.to_csv(trade_log_path, index=False)
    print(f"✅ Trade-Log gespeichert in: {trade_log_path}")

    # KPIs
    total_trades = len(trades_df)
    wins = trades_df[trades_df["pnl"] > 0]
    losses = trades_df[trades_df["pnl"] <= 0]
    win_rate = len(wins) / total_trades if total_trades else 0
    avg_win = wins["pnl"].mean() if not wins.empty else 0
    avg_loss = losses["pnl"].mean() if not losses.empty else 0
    profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float("inf")

    # Max Drawdown (simplified over equity)
    equity_curve = trades_df["equity_end"].cummax() - trades_df["equity_end"]
    max_drawdown = equity_curve.max()

    performance = {
        "total_trades": total_trades,
        "win_rate": round(win_rate, 4),
        "avg_win": round(avg_win, 4),
        "avg_loss": round(avg_loss, 4),
        "profit_factor": round(profit_factor, 4),
        "max_drawdown": round(max_drawdown, 4),
        "final_equity": round(trades_df["equity_end"].iloc[-1], 4),
    }

    # Save JSON
    perf_path = os.path.join(output_dir, "performance.json")
    with open(perf_path, "w") as f:
        json.dump(performance, f, indent=4)
    print(f"📊 Performance-Daten gespeichert in: {perf_path}")

    return trades_df, performance
