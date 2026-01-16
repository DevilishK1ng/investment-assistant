import os
import requests

def send_telegram(message: str):
    """
    Envía un mensaje de texto a Telegram usando un bot.
    """
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        print("Error enviando mensaje a Telegram:", response.text)

def send_telegram_image(image_path, caption=""):

    TOKEN = st.secrets["telegram"]["bot_token"]
    CHAT_ID = st.secrets["telegram"]["chat_id"]
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    with open(image_path, "rb") as img:
        files = {"photo": img}
        data = {
            "chat_id": CHAT_ID,
            "caption": caption
        }
        response = requests.post(url, data=data, files=files)

    if response.status_code != 200:
        raise RuntimeError(response.text)
