import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from handlers.main import router
import os

token = os.environ["TOKEN"]


buttons = [
    types.BotCommand(description="Поиск видео по тесктовому запросу", command="/search"),
    types.BotCommand(description="Загрузка видео", command="/upload")
]


async def main():
    logging.basicConfig(
        level=logging.INFO,
        #filename="log.log",
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=token)

    await bot.set_my_commands(commands=buttons)

    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
