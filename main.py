import os
import asyncio
from datetime import datetime, timedelta, time, timezone
from telegram import Bot

BOT_TOKEN = "7857747352:AAGL6XXQyZlj-6k_U6BV-rFF2wacDRdGjVE"  # или os.getenv("BOT_TOKEN")
CHAT_ID = "-1002700138488"        # или os.getenv("CHAT_ID")

VACATION_DATE = datetime(2025, 7, 27, 14, 39, 0, tzinfo=timezone.utc)  # дата и время отпуска (UTC)

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

        # Рассчитаем сколько секунд ждать до следующего 11:00 UTC
        target_time_today = datetime.combine(now.date(), time(14, 39, 0, tzinfo=timezone.utc))
        if now < target_time_today:
            wait_seconds = (target_time_today - now).total_seconds()
        else:
            # если уже позже 11:00, ждём до завтра 11:00
            target_time_tomorrow = target_time_today + timedelta(days=1)
            wait_seconds = (target_time_tomorrow - now).total_seconds()

        await asyncio.sleep(wait_seconds)

if __name__ == "__main__":
    asyncio.run(send_countdown())
