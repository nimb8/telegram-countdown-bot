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
    return "Бот работает!"

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
        return  # Событие прошло

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        response = requests.post(url, data={"chat_id": chat_id, "text": text})
        if not response.ok:
            print(f"Ошибка отправки сообщения: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Исключение при отправке сообщения: {e}")

def scheduler(token, chat_id):
    while True:
        now = datetime.datetime.utcnow()
        if now.hour == 11 and now.minute == 0:
            send_message(token, chat_id)
            time.sleep(60)  # чтобы не отправлять несколько раз в одну минуту
        else:
            time.sleep(30)  # проверяем каждые 30 секунд

if __name__ == "__main__":
    print("Переменные окружения в контейнере:")
    for k, v in os.environ.items():
        print(f"{k} = {v}")

    TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    if not TOKEN or not CHAT_ID:
        print("Ошибка: Не заданы переменные окружения BOT_TOKEN или CHAT_ID")
        sys.exit(1)

    threading.Thread(target=scheduler, args=(TOKEN, CHAT_ID), daemon=True).start()

    app.run(host="0.0.0.0", port=3000, debug=False)
