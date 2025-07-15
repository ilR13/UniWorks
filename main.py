import asyncio
import logging
from aiogram import Dispatcher, types, Bot
from handlers import router
from bot import bot
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота

dp = Dispatcher()
# bot = Bot(token="8096513053:AAFBJCm5NR91df5eaK_jv1W6Kb_SwOTLxTY")


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Exit")