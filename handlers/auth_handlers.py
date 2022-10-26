from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from createbot import bot

from custom_keyboard import keyb
from databaseconnection import DatabaseConnection
from config import host, db_name, password, user


database = ''


async def distrib_references(msg: types.Message):
    if user_update(msg):
        await msg.reply('Вы подписались на рассылку')
    else:
        await msg.reply('Вы отписались от рассылки')


def user_update(message):
    global database # global variable for a content database object

    try:
        database = DatabaseConnection(
            host=host,
            user=user,
            password=password,
            db_name=db_name
        )

        return database.update_data(message.from_user.id)
    except Exception as exc:
        print(f'[INFO] PostgresSQL auth error, {exc}')
        return False
    finally:
        print('[INFO] PostgresSQL connection closed')


def auth_handlers_register(dp: Dispatcher):
    dp.register_message_handler(distrib_references, commands=['reference'])

