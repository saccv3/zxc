from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from custom_keyboard import keyb
from databaseconnection import DatabaseConnection
from config import host, db_name, password, user

message_chat_id = ''


class UserBot(StatesGroup):
    user_phone_contact = State()
    user_chat_id = ''


async def begin_reg(call_back: types.CallbackQuery):
    global message_chat_id
    await call_back.message.answer(
        "Для регистрации пользователя необходимо отправить номер телефона",
        reply_markup=keyb.phone_number_kb
    )

    message_chat_id = call_back.message.chat.id
    await UserBot.next()


async def put_phone_user(message: types.Contact, state: FSMContext):
    async with state.proxy() as data:
        data['user_phone_contact'] = message.contact.phone_number
        data['user_chat_id'] = message.contact.user_id

    print(data)
    await state.finish()


def reg_handlers_register(dp: Dispatcher):
    dp.register_callback_query_handler(begin_reg, text='reg_user', state=None)
    dp.register_message_handler(put_phone_user, content_types=['contact'], state=UserBot.user_phone_contact)
