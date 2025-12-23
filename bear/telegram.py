import os, requests
from dotenv import load_dotenv
load_dotenv()

TOKEN   = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def teddy_say(text):
    """Send a message to Telegram with teddy bear emoji"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': f"🧸 {text}"}
    try:
        r = requests.post(url, json=payload, timeout=5)
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"Telegram error: {e}")
        return False