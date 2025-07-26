import pandas as pd
from strategies.sma_crossover import sma_strategy
from backtesting.backtester import backtest_strategy
import itertools
import os

# Datei einlesen
df = pd.read_csv("data/btcusdt_1h.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df.set_index("timestamp", inplace=True)

# Grid-Search Parameter
short_windows = range(5, 12)  # z. B. 5–11
long_windows = range(10, 16)  # z. B. 10–15

results = []

# Grid Search
for short, long in itertools.product(short_windows, long_windows):
    if short >= long:
        continue  # nur sinnvolle Kombinationen testen

    params = {"short_window": short, "long_window": long}
    result = backtest_strategy(df, lambda df_: sma_strategy(df_, **params))

    results.append({
        "short_window": short,
        "long_window": long,
        "return": result.get("return", 0)
    })

# Ergebnisse sortierens
results_df = pd.DataFrame(results)
results_df.sort_values(by="return", ascending=False, inplace=True)

# Speichern
os.makedirs("data", exist_ok=True)
results_df.to_csv("data/sma_grid_results.csv", index=False)

# Ausgabe
print("📊 Beste Ergebnisse:")
print(results_df.head(10))
print("✅ Ergebnisse gespeichert in: data/sma_grid_results.csv")
