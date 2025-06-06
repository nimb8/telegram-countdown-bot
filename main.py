from flask import Flask
import threading
import time
import datetime
import requests
import os
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!!"

# Дата события (например, отпуск)
event_date = datetime.date(2025, 7, 27)

def get_days_left():
    today = datetime.date.today()
    delta = event_date - today
    return delta.days

def send_message(token, chat_id):
    days = get_days_left()
    if days > 0:
        text = f"До отпуска осталось {days} дн."
    elif days == 0:
        text = "Отпуск начинается сегодня!!!"
    else:
        return  # Если событие прошло, не отправляем сообщение

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        response = requests.post(url, data={"chat_id": chat_id, "text": text})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при отправке сообщения: {e}")

def scheduler(token, chat_id):
    while True:
        now = datetime.datetime.utcnow()
        if now.hour == 11 and now.minute == 0:
            send_message(token, chat_id)
            time.sleep(60)
        time.sleep(30)

if __name__ == "__main__":
    print("Переменные окружения в контейнере:")
    for k, v in os.environ.items():
        print(f"{k}={v}")

    TOKEN = os.environ.get("BOT_TOKEN")
    CHAT_ID = os.environ.get("CHAT_ID")

    if not TOKEN or not CHAT_ID:
        print("Ошибка: Не заданы переменные окружения BOT_TOKEN или CHAT_ID")
        sys.exit(1)

    threading.Thread(target=scheduler, args=(TOKEN, CHAT_ID), daemon=True).start()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
