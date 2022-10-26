from createbot import dp
from aiogram import executor
from handlers import basic_handlers, reg_handlers, auth_handlers

try:
    async def on_activate(_):
        print('[INFO] Бот вышел в онлайн')

    auth_handlers.auth_handlers_register(dp)
    basic_handlers.basic_handlers_register(dp)
    reg_handlers.reg_handlers_register(dp)

    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_activate
    )
except Exception as e:
    print('[INFO] Возникла ошибка! ', e)

finally:
    print('[INFO] Работа бота приостановлена')
