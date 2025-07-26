import pandas as pd
import matplotlib.pyplot as plt

from indicators.technical_indicators import calculate_rsi, calculate_bollinger_bands

# 🔹 Daten einlesen
df = pd.read_csv('data/btcusdt_1h.csv', parse_dates=['timestamp'])
df.set_index('timestamp', inplace=True)

# 🔹 Indikatoren berechnen
df['rsi'] = calculate_rsi(df, period=14)
df['bb_upper'], df['bb_mid'], df['bb_lower'] = calculate_bollinger_bands(df, period=20)

# 🔹 Letzte Werte anzeigen
print("\n📊 Letzte Werte:")
print(df[['close', 'rsi', 'bb_upper', 'bb_mid', 'bb_lower']].tail(10))

# 🔹 Plotten (optional)
df[['close', 'bb_upper', 'bb_mid', 'bb_lower']].tail(150).plot(figsize=(12, 6), title='Bollinger Bands')
plt.show()

df[['rsi']].tail(150).plot(figsize=(12, 3), title='RSI (14)', color='purple')
plt.axhline(70, color='red', linestyle='--')
plt.axhline(30, color='green', linestyle='--')
plt.show()
