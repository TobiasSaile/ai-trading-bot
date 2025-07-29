import logging
import pandas as pd
from models.predictor import predict_signal

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

class PaperTrader:
    def __init__(self, initial_balance=10_000, trading_fee=0.001):
        self.balance = initial_balance
        self.position = 0  # ETH-Menge
        self.trading_fee = trading_fee
        self.portfolio_value = initial_balance
        self.logs = []
        self.portfolio_value_series = []

    def update_portfolio_value(self, price):
        self.portfolio_value = self.balance + self.position * price
        self.portfolio_value_series.append(self.portfolio_value)

    def buy(self, price, timestamp):
        if self.position == 0:
            amount = self.balance * (1 - self.trading_fee) / price
            self.position = amount
            self.balance = 0
            self.update_portfolio_value(price)
            message = f"[{timestamp}] ✅ BUY @ {price:.2f} | ETH: {self.position:.4f}"
            self.logs.append(message)
            logging.info(message)

    def sell(self, price, timestamp):
        if self.position > 0:
            proceeds = self.position * price * (1 - self.trading_fee)
            self.balance = proceeds
            self.position = 0
            self.update_portfolio_value(price)
            message = f"[{timestamp}] ❌ SELL @ {price:.2f} | Balance: {self.balance:.2f}"
            self.logs.append(message)
            logging.info(message)

    def run_with_model(self, df: pd.DataFrame):
        df = df.dropna().copy()
        self.portfolio_value_series.clear()

        for i, row in df.iterrows():
            price = row['close']
            timestamp = row['timestamp']
            signal = predict_signal()  # Klassifikation: BUY, SELL oder HOLD

            if signal == "BUY":
                self.buy(price, timestamp)
            elif signal == "SELL":
                self.sell(price, timestamp)
            else:
                self.update_portfolio_value(price)  # Für Equity-Kurve auch bei HOLD

        # Am Ende alles verkaufen (close position)
        if self.position > 0:
            self.sell(df.iloc[-1]['close'], df.iloc[-1]['timestamp'])

        summary = f"📊 Final Portfolio Value (Model): {self.portfolio_value:.2f} USDT"
        self.logs.append(summary)
        logging.info(summary)

        return self.logs, self.portfolio_value
