import tkinter as tk
from tkinter import ttk
import threading
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys, os

# Hauptordner zum Pfad hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from paper_trading.paper_trader import PaperTrader
from data.binance_fetcher import fetch_eth_usdt_ohlcv
from features.feature_engineering import add_features
from visuals.plot_trading_signals import plot_signals_and_equity


class TradingBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Crypto Trading Bot")
        self.root.geometry("900x700")

        self.trader = None
        self.df = None

        self.setup_ui()

    def setup_ui(self):
        # Header
        ttk.Label(self.root, text="💹 AI Trading Bot Dashboard", font=("Arial", 20)).pack(pady=8)

        # Portfolio-Anzeige
        info_frame = ttk.Frame(self.root)
        info_frame.pack()
        self.balance_var = tk.StringVar(value="Balance: 0.00 USDT")
        self.position_var = tk.StringVar(value="Position: 0.000000 ETH")
        self.value_var = tk.StringVar(value="Portfolio Value: 0.00 USDT")
        ttk.Label(info_frame, textvariable=self.balance_var).grid(row=0, column=0, padx=10)
        ttk.Label(info_frame, textvariable=self.position_var).grid(row=0, column=1, padx=10)
        ttk.Label(info_frame, textvariable=self.value_var).grid(row=0, column=2, padx=10)

        # Strategie-Wahl & Start-Button
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        ttk.Label(control_frame, text="Strategie:").grid(row=0, column=0, padx=(0,5))
        self.strategy_var = tk.StringVar(value="Model")
        ttk.Combobox(control_frame, textvariable=self.strategy_var, values=["Model", "SMA"], width=10).grid(row=0, column=1)
        self.start_btn = ttk.Button(control_frame, text="▶️ Start Paper-Trading", command=self.start_trading)
        self.start_btn.grid(row=0, column=2, padx=20)

        # Log-Feld
        self.log_text = tk.Text(self.root, height=10, width=105)
        self.log_text.pack(pady=5)

        # Chart-Bereich
        self.fig, self.ax = plt.subplots(figsize=(8,3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    def start_trading(self):
        # Button deaktivieren und Log leeren
        self.start_btn.config(state=tk.DISABLED)
        self.log_text.delete(1.0, tk.END)
        self.ax.clear()
        self.log("🔄 Starte Feature-Berechnung & Modellvorhersage...")

        def run():
            # 1️⃣ Live-Daten holen & Features bauen
            self.df = fetch_eth_usdt_ohlcv()
            self.df = add_features(self.df).dropna()

            # 2️⃣ Trader starten
            self.trader = PaperTrader()
            strat = self.strategy_var.get()
            if strat == "SMA":
                logs, value = self.trader.run(self.df)
            else:
                logs, value = self.trader.run_with_model(self.df)

            # 3️⃣ UI updaten
            self.update_ui()
            for line in logs:
                self.log(line)
            self.log(f"\n📈 Endwert: {value:.2f} USDT")

            # 4️⃣ Chart: Portfolio Equity oder Buy/Sell-Signale
            self.ax.clear()
            if hasattr(self.trader, 'trade_log'):
                # Falls trade_log existiert, Signale darstellen
                plot_signals(self.df, self.trader.trade_log, ax=self.ax)
            else:
                # Fallback: kumulative Rendite darstellen
                r = self.df['close'].pct_change().fillna(0).cumsum()
                self.ax.plot(self.df['timestamp'], r, label="Equity (Close-CumReturn)")
                self.ax.set_title("📈 Kumulative Rendite")

            self.ax.legend()
            self.canvas.draw()

            # Button wieder aktivieren
            self.start_btn.config(state=tk.NORMAL)

        threading.Thread(target=run, daemon=True).start()

    def update_ui(self):
        self.balance_var.set(f"Balance: {self.trader.balance:.2f} USDT")
        self.position_var.set(f"Position: {self.trader.position:.6f} ETH")
        self.value_var.set(f"Portfolio Value: {self.trader.portfolio_value:.2f} USDT")

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotGUI(root)
    root.mainloop()
