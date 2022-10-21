from aiogram import types, Dispatcher
from custom_keyboard import keyb


async def begin_tell(message: types.Message):
    if message.from_user.id == message.chat.id:
        await message.answer(
            f"<b>Доброго времени суток! {message.from_user.first_name}</b>\n\n" +
            "Мы поможем зарегистрировать твой аккаунт у нас на сайте, а также:\n" +
            "* Позволим удобно получать персональные данные.\n" +
            "* Сохранять документы и скачивать их.\n" +
            "* Быстро и удобно связываться с преподавателями.\n",
            reply_markup=keyb.main_menu,
            parse_mode=types.ParseMode.HTML)

        print(message)
    else:
        await message.answer(
            'Для продолжения диалога напишите боту в личные сообщения..',
            reply_markup=keyb.sub_menu
        )


def basic_handlers_register(dp: Dispatcher):
    dp.register_message_handler(begin_tell, commands=['start'])
