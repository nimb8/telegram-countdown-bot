import os
import time
from datetime import datetime, timedelta
from telegram import Bot

# Хардкодим переменные для проверки
BOT_TOKEN = "7857747352:AAGL6XXQyZlj-6k_U6BV-rFF2wacDRdGjVE"
CHAT_ID = "-1002700138488"

bot = Bot(token=BOT_TOKEN)

def get_seconds_until_target(target_datetime):
    now = datetime.utcnow()
    delta = target_datetime - now
    return max(0, int(delta.total_seconds()))

def format_countdown(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{days} дн {hours} ч {minutes} м {secs} с"

def main():
    # Укажи дату и время цели в UTC
    target = datetime(2025, 7, 26, 23, 59, 59)

    while True:
        seconds_left = get_seconds_until_target(target)
        message = f"До отпуска осталось: {format_countdown(seconds_left)}"
        try:
            bot.send_message(chat_id=CHAT_ID, text=message)
            print(f"Отправлено сообщение: {message}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()
