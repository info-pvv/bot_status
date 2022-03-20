#!venv/bin/python
import logging
import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import BotCommand

from aiogram.utils.exceptions import BotBlocked
import aiogram.utils.markdown as fmt

from config import TOKEN
from app.handlers.health import register_handlers_health
from app.handlers.common import register_handlers_common
from app.handlers.admin import register_handlers_admin

logger = logging.getLogger(__name__)

acc_zd=0
acc_bol=0



logging.basicConfig(level=logging.INFO)



# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Парсинг файла конфигурации
    #config = load_config("config/bot.ini")
    bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())
    
    #
    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_health(dp)
    register_handlers_admin(dp)

    # Установка команд бота
    await set_commands(bot)

    
    @dp.message_handler(lambda message: message.text == "Жрать")
    async def with_puree1(message: types.Message):
        await message.reply("Дома пожрешь")
    


    @dp.errors_handler(exception=BotBlocked)
    async def error_bot_blocked(update: types.Update, exception: BotBlocked):
       print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
       return True
    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()




if __name__ == "__main__":
    asyncio.run(main())
    #executor.start_polling(dp, skip_updates=True)
