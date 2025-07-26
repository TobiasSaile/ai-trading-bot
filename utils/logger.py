import os
import csv
from datetime import datetime

LOG_DIR = "logs"
SESSION_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = os.path.join(LOG_DIR, f"session_{SESSION_ID}.csv")

def init_log():
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp", "action", "price", 
            "sma_short", "sma_long", 
            "position", "position_size", 
            "equity", "return", "strategy"
        ])

def log_trade(timestamp, action, price, sma_short, sma_long, position, position_size, equity, ret, strategy_id):
    if any(x is None for x in [timestamp, price, sma_short, sma_long]):
        return  # Nichts loggen, wenn Daten unvollständig

    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            timestamp,
            action,
            round(price, 2),
            round(sma_short, 2),
            round(sma_long, 2),
            position,
            position_size,
            round(equity, 4),
            round(ret, 6),
            strategy_id
        ])
    print(f"[{timestamp}] {action.upper()} @ {price:.2f} | SMA {sma_short:.2f}/{sma_long:.2f} | Equity: {equity:.4f}")
