import pandas as pd
import logging
from models.predictor import predict_signal

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

class PaperTrader:
    def __init__(self, initial_balance=10_000, trading_fee=0.001):
        self.balance = initial_balance
        self.position = 0
        self.trading_fee = trading_fee
        self.portfolio_value = initial_balance
        self.logs = []

    def update_portfolio_value(self, price):
        self.portfolio_value = self.balance + self.position * price

    def buy(self, price, timestamp):
        if self.position == 0:
            amount = self.balance * (1 - self.trading_fee) / price
            self.position = amount
            self.balance = 0
            self.update_portfolio_value(price)
            self.logs.append(f"[{timestamp}] BUY @ {price:.2f} | BTC: {self.position:.4f}")
            logging.info(f"BUY @ {price:.2f} | BTC: {self.position:.4f}")

    def sell(self, price, timestamp):
        if self.position > 0:
            proceeds = self.position * price * (1 - self.trading_fee)
            self.balance = proceeds
            self.position = 0
            self.update_portfolio_value(price)
            self.logs.append(f"[{timestamp}] SELL @ {price:.2f} | Balance: {self.balance:.2f}")
            logging.info(f"SELL @ {price:.2f} | Balance: {self.balance:.2f}")

    def run_with_model(self, df):
        df.dropna(inplace=True)
        for i, row in df.iterrows():
            price = row['close']
            ts = row['timestamp']
            signal = predict_signal()
            if signal == "BUY":
                self.buy(price, ts)
            elif signal == "SELL":
                self.sell(price, ts)
        if self.position > 0:
            self.sell(df.iloc[-1]['close'], df.iloc[-1]['timestamp'])
        logging.info(f"📊 Final Portfolio Value (Model): {self.portfolio_value:.2f} USDT")
        return self.logs, self.portfolio_value

if __name__ == "__main__":
    df = pd.read_csv("data/btcusdt_1h.csv")
    trader = PaperTrader()
    trader.run_with_model(df)
