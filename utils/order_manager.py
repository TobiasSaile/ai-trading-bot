# utils/order_manager.py
from config.config import TRADE_QUANTITY_USDT, TRADING_MODE, SYMBOL
from live_trading.mexc_api import place_order

def execute_trade(signal):
    if TRADING_MODE == "PAPER":
        print(f"[PAPER] Signal: {signal}")
        return

    if signal == "BUY":
        place_order(SYMBOL, "BUY", TRADE_QUANTITY_USDT)
    elif signal == "SELL":
        place_order(SYMBOL, "SELL", TRADE_QUANTITY_USDT)
    else:
        print(f"ℹ️ Kein Trade bei Signal: {signal}")
