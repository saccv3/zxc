from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from createbot import bot

from custom_keyboard import keyb
from databaseconnection import DatabaseConnection
from config import host, db_name, password, user


database = ''


class UserBot(StatesGroup):
    user_phone_contact = State()
    user_chat_id = ''


async def begin_reg(call_back: types.CallbackQuery):
    await call_back.message.answer(
        "Для регистрации пользователя необходимо отправить номер телефона",
        reply_markup=keyb.phone_number_kb
    )

    await UserBot.next()


async def put_phone_user(message: types.Contact, state: FSMContext):
    async with state.proxy() as data:
        data['user_phone_contact'] = message.contact.phone_number
        data['user_chat_id'] = message.contact.user_id

    print(data)

    if create_database_connection(data):
        bot.send_message(
            message.contact.user_id,
            f'Регистрация прошла успешно! Спасибо, {message.contact.first_name}'
        )

    await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.finish()
    await message.reply('Ок!')


def create_database_connection(data):
    global database

    try:
        database = DatabaseConnection(
            host=host,
            user=user,
            password=password,
            db_name=db_name
        )

        database.put_data_user_table(data)

    except Exception as exc:
        print(f'[INFO] PostgresSQL registration error, {exc}')
    finally:
        if database.get_connection():
            database.close_connection()


def reg_handlers_register(dp: Dispatcher):
    dp.register_callback_query_handler(begin_reg, text='reg_user', state=None)
    dp.register_message_handler(put_phone_user, content_types=['contact'], state=UserBot.user_phone_contact)
    dp.register_message_handler(cancel_handler, state="*", commands='выход')
    dp.register_message_handler(cancel_handler, Text(equals='выход', ignore_case=True), state="*")
