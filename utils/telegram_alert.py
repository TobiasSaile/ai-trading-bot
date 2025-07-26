import requests

# Deine persönlichen Daten
TELEGRAM_TOKEN = "DEIN_BOT_TOKEN"
CHAT_ID = "DEINE_CHAT_ID"

def send_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if not response.ok:
            print(f"❌ Telegram-Error: {response.text}")
    except Exception as e:
        print(f"❌ Telegram-Ausfall: {e}")
