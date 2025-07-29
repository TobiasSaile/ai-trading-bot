# live_trading/mexc_api.py
import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
from config.config import MEXC_API_KEY, MEXC_SECRET_KEY

BASE_URL = "https://api.mexc.com"

def sign_request(params):
    query_string = urlencode(params)
    signature = hmac.new(
        MEXC_SECRET_KEY.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"{query_string}&signature={signature}"

def place_order(symbol, side, quantity):
    timestamp = int(time.time() * 1000)
    endpoint = "/api/v3/order"
    url = BASE_URL + endpoint
    params = {
        "symbol": symbol,
        "side": side.upper(),  # BUY / SELL
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": timestamp
    }
    headers = {
        "X-MEXC-APIKEY": MEXC_API_KEY
    }
    signed_query = sign_request(params)
    try:
        response = requests.post(url, headers=headers, data=signed_query)
        data = response.json()
        print(f"✅ Order {side} ausgeführt: {data}")
        return data
    except Exception as e:
        print(f"❌ Fehler bei Order {side}: {e}")
        return None
