import requests
from config.settings import TELEGRAM_BOT_TOKEN

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_telegram_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    try:
        requests.post(TELEGRAM_API_URL, data=data, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")