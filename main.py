import os
import asyncio
from datetime import datetime, timezone

from telegram import Bot

BOT_TOKEN = "7857747352:AAGL6XXQyZlj-6k_U6BV-rFF2wacDRdGjVE"  # или os.getenv("BOT_TOKEN")
CHAT_ID = "-1002700138488"        # или os.getenv("CHAT_ID")

async def main():
    bot = Bot(token=BOT_TOKEN)
    now = datetime.now(timezone.utc)
    vacation_date = datetime(2025, 7, 1, tzinfo=timezone.utc)  # например, дата отпуска
    diff = vacation_date - now

    days = diff.days
    seconds = diff.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    message = f"До отпуска осталось: {days} дн {hours} ч {minutes} м {seconds} с"

    await bot.send_message(chat_id=CHAT_ID, text=message)
    print("Отправлено сообщение:", message)

if __name__ == "__main__":
    asyncio.run(main())

