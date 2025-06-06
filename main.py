import os
import asyncio
from datetime import datetime, timedelta, time, timezone
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

VACATION_DATE = datetime(2025, 7, 27, 11, 0, 0, tzinfo=timezone.utc)  # дата и время отпуска в UTC

async def send_countdown():
    bot = Bot(token=BOT_TOKEN)

    while True:
        now = datetime.now(timezone.utc)

        if now >= VACATION_DATE:
            await bot.send_message(chat_id=CHAT_ID, text="Отпуск начинается!!!")
            print("Отправлено: Отпуск начинается!!!")
            break

        # Вычисляем сколько осталось
        diff = VACATION_DATE - now
        days = diff.days
        seconds = diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        message = f"До отпуска осталось: {days} дн {hours} ч {minutes} м {seconds} с"
        await bot.send_message(chat_id=CHAT_ID, text=message)
        print("Отправлено:", message)

        # Рассчитываем время до следующего 11:00 UTC
        target_time_today = datetime.combine(now.date(), time(11, 0, 0, tzinfo=timezone.utc))
        if now < target_time_today:
            wait_seconds = (target_time_today - now).total_seconds()
        else:
            target_time_tomorrow = target_time_today + timedelta(days=1)
            wait_seconds = (target_time_tomorrow - now).total_seconds()

        print(f"Ждем до {target_time_today.isoformat() if now < target_time_today else target_time_tomorrow.isoformat()} (еще {int(wait_seconds)} секунд)")
        await asyncio.sleep(wait_seconds)

if __name__ == "__main__":
    asyncio.run(send_countdown())
