import os
import asyncio
from datetime import datetime, timedelta, time, timezone
from telegram import Bot

BOT_TOKEN = "7857747352:AAGL6XXQyZlj-6k_U6BV-rFF2wacDRdGjVE"  # или os.getenv("BOT_TOKEN")
CHAT_ID = "-4874063053"        # или os.getenv("CHAT_ID")

VACATION_DATE = datetime(2025, 7, 27, 15, 02, 0, tzinfo=timezone.utc)  # дата и время отпуска (UTC)

async def send_countdown():
    bot = Bot(token=BOT_TOKEN)

    while True:
        now = datetime.now(timezone.utc)

        if now >= VACATION_DATE:
            await bot.send_message(chat_id=CHAT_ID, text="Отпуск начинается!!!")
            print("Отправлено: Отпуск начинается!!!")
            break

        # Рассчитаем сколько осталось
        diff = VACATION_DATE - now

        days = diff.days
        seconds = diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        message = f"До отпуска осталось: {days} дн {hours} ч {minutes} м {seconds} с"

        # Определяем момент следующей отправки — 14:53 UTC каждый день
        target_time_today = datetime.combine(now.date(), time(15, 02, 0, tzinfo=timezone.utc))
        if now < target_time_today:
            wait_seconds = (target_time_today - now).total_seconds()
            # Ждем до target_time_today, не отправляем сообщение сразу
            print(f"Ждем до {target_time_today.isoformat()} (еще {wait_seconds:.0f} секунд)")
            await asyncio.sleep(wait_seconds)
            await bot.send_message(chat_id=CHAT_ID, text=message)
            print("Отправлено:", message)
        else:
            # Если уже после target_time_today, ждем до следующего дня
            target_time_tomorrow = target_time_today + timedelta(days=1)
            wait_seconds = (target_time_tomorrow - now).total_seconds()
            print(f"Ждем до {target_time_tomorrow.isoformat()} (еще {wait_seconds:.0f} секунд)")
            await asyncio.sleep(wait_seconds)

if __name__ == "__main__":
    asyncio.run(send_countdown())
