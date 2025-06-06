from flask import Flask
import threading
import time
import datetime
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

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
    requests.post(url, data={"chat_id": chat_id, "text": text})

def scheduler(token, chat_id):
    while True:
        now = datetime.datetime.utcnow()
        if now.hour == 11 and now.minute == 0:
            send_message(token, chat_id)
            time.sleep(60)
        time.sleep(30)

if __name__ == "__main__":
    # Читаем переменные только при запуске
    TOKEN = os.environ["BOT_TOKEN"]
    CHAT_ID = os.environ["CHAT_ID"]

    # Запускаем планировщик
    threading.Thread(target=scheduler, args=(TOKEN, CHAT_ID), daemon=True).start()

    # Запускаем Flask
    app.run(host="0.0.0.0", port=3000)
