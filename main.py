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

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

event_date = datetime.date(2025, 7, 27)

def get_days_left():
    today = datetime.date.today()
    delta = event_date - today
    return delta.days

def send_message():
    days = get_days_left()
    if days > 0:
        text = f"До отпуска осталось {days} дн."
    elif days == 0:
        text = "Отпуск начинается сегодня!!!"
    else:
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def scheduler():
    while True:
        now = datetime.datetime.utcnow()
        if now.hour == 11 and now.minute == 0:
            send_message()
            time.sleep(60)
        time.sleep(30)

threading.Thread(target=scheduler, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
