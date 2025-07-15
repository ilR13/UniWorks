import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from handlers import router


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="8096513053:AAFBJCm5NR91df5eaK_jv1W6Kb_SwOTLxTY")
dp = Dispatcher()



async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Exit")