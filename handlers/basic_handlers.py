from aiogram import types, Dispatcher
from custom_keyboard import keyb
from createbot import bot

from custom_keyboard import keyb
from databaseconnection import DatabaseConnection
from config import host, db_name, password, user

database = '' # global variable for a save base connect object


# method called when writing the /start option
# The method sends the primary form to the user depending on whether the user is logged in or not.
async def begin_tell(message: types.Message):
    if message.from_user.id == message.chat.id:
        if user_was_reg(message):  # database query to find the user
            await message.answer(
                f"<b>Доброго времени суток! {message.from_user.first_name}</b>\n\n" +
                "Мы поможем зарегистрировать твой аккаунт у нас на сайте, а также:\n" +
                "* Позволим удобно получать персональные данные.\n" +
                "* Сохранять документы и скачивать их.\n" +
                "* Быстро и удобно связываться с преподавателями.\n",
                reply_markup=keyb.main_menu,
                parse_mode=types.ParseMode.HTML)
        else:
            await message.reply(
                f"<b>Доброго времени суток! {message.from_user.first_name}</b>\n\n" +
                "<b>Помощь:</b> \n" +
                "/help - получить контактные данные \n\n" +
                "<b>Рассылка:</b>\n" +
                "/message_chat - Сообщения от пользователей \n" +
                "/reference {:>5s}\n".format("- Рассылка новостей"),
                parse_mode=types.ParseMode.HTML)

        print(message)
    else:
        await message.answer(
            'Для продолжения диалога напишите боту в личные сообщения..',
            reply_markup=keyb.sub_menu
        )


# database query to find the user
# A one-time connection is created in the database and closed when the function body is executed
def user_was_reg(message):
    global database # global variable for a content database object

    try:
        database = DatabaseConnection(
            host=host,
            user=user,
            password=password,
            db_name=db_name
        )

        # boola = not database.find_table_content(message.from_user.id)
        # print(f'{boola} blyad try except')
        return not database.find_table_content(message.from_user.id)  # query
    except Exception as exc:
        print(f'[INFO] PostgresSQL auth error, {exc}')
        return False
    finally:
        print('[INFO] PostgresSQL connection closed')


async def send_help(msg: types.Message):
    await msg.reply(
        help_information(),
        parse_mode=types.ParseMode.HTML
    )


def help_information():
    return "<b>Костанайский инженерно-экономический университет им. М. Дулатова</b> \n \n" + \
           "<b>Адрес</b> \n" \
           + "Улица Чернышевского 59, Костанай 110000, Казахстан \n\n" + \
           "<b>Телефон</b> \n" + \
           "+7 777 581 5509 \n\n"


# function for a registered other function's and callback method's
def basic_handlers_register(dp: Dispatcher):
    dp.register_message_handler(begin_tell, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])

