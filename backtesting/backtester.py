import pandas as pd
from strategies.sma_crossover import sma_strategy
from utils.logger import init_log, log_trade
from analyzer.performance import analyze_trades

# log_df = DataFrame mit ENTRY/REVERSE-Logs (inkl. price, timestamp, equity, action)
analyze_trades(log_df)

# 1️⃣ Parameter
short_window = 5
long_window = 15
strategy_id = f"SMA_{short_window}_{long_window}"
position_size = 1.0
capital = 10000

# 2️⃣ Daten laden
df = pd.read_csv("data/btcusdt_1h.csv", parse_dates=["timestamp"])

# 3️⃣ Strategie anwenden
df = sma_strategy(df, short_window=short_window, long_window=long_window)
df['returns'] = df['close'].pct_change()
df['strategy'] = df['position'].shift(1) * df['returns']
df['equity'] = df['strategy'].cumsum()

# 4️⃣ Log vorbereiten
init_log()

# 5️⃣ Trading Loop
prev_position = 0

for i in range(1, len(df)):
    current_position = df['position'].iloc[i]
    timestamp = df['timestamp'].iloc[i]
    price = df['close'].iloc[i]
    sma_s = df['sma_short'].iloc[i]
    sma_l = df['sma_long'].iloc[i]
    equity = df['equity'].iloc[i]
    ret = df['strategy'].iloc[i]

    action = None

    # ENTRY (von flat in Position)
    if prev_position == 0 and current_position != 0:
        action = "entry"

    # CLOSE (von Position auf flat)
    elif prev_position != 0 and current_position == 0:
        action = "close"

    # REVERSE (Positionswechsel von long → short oder umgekehrt)
    elif prev_position != 0 and current_position != prev_position and current_position != 0:
        action = "reverse"

    if action:
        log_trade(
            timestamp=timestamp,
            action=action,
            price=price,
            sma_short=sma_s,
            sma_long=sma_l,
            position=current_position,
            position_size=position_size,
            equity=equity,
            ret=ret,
            strategy_id=strategy_id
        )

    prev_position = current_position
