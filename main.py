import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="8096513053:AAFBJCm5NR91df5eaK_jv1W6Kb_SwOTLxTY")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.id != 5335241383:
        await message.answer("Hello!" + str(message.from_user.first_name))
    else:
        await message.answer("Hello Oleg")

# Запуск процесса поллинга новых апдейтов
async def main():

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())