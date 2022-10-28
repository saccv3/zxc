from aiogram import types, Dispatcher
from createbot import bot

from custom_keyboard import keyb
from databaseconnection import DatabaseConnection
from config import host, db_name, password, user

database = ''
is_album = False
message_caption = ''
album = []


# function for writing a message to the newsletter
async def begin_distrib_form(call: types.CallbackQuery):
    global is_album
    is_album = True

    await call.message.answer(
        '<b>Оформление поста для рассылки\n\n</b>' +
        "- Пришлите картинки \n" +
        "- Оставьте подпись, которая и будет использоваться в качестве текста \n\n" +
        "/send - начать рассылку",
        parse_mode=types.ParseMode.HTML
    )


# subscription check function
async def distrib_references(msg: types.Message):
    if user_update(msg):
        await msg.reply('Вы подписались на рассылку')
    else:
        await msg.reply('Вы отписались от рассылки')


async def collect_data(message: types.Message):
    global message_caption
    if is_album:
        print('Картинка добавлена')
        album.append(message.photo[-1].file_id)
        if message.caption:
            print(message.caption)
            message_caption = message.caption


async def album_send(message: types.Message):
    global is_album
    global message_caption

    if message.text == '/send':
        if len(album) > 0:
            album_arr = types.MediaGroup()

            # заполнения альбома для рассылки и установка на последний элемент подписи
            for i in album:
                if i == album[-1]:
                    album_arr.attach_photo(i, caption=message_caption)
                    break
                album_arr.attach_photo(i)

            error_chat_id = ''

            try:
                for obj in user_refrences_sub():
                    error_chat_id = obj[0]
                    await bot.send_media_group(obj[0], album_arr)
            except Exception as exc:
                print(f'[INFO] Send message error {exc}, chat_id={error_chat_id}')

            album.clear()
            is_album = False

            await message.answer('Рассылка успешно отправлена.')
        else:
            await message.answer('Список элементов для поста пуст. \n Попробуйте прислать картинки.')
    else:
        await message.answer('Рассылка остановлена. Попробуйте заного.')


# _________________________________DATABASE CONNECTION________________________________#


# query subscription
def user_update(message):
    global database  # global variable for a content database object

    try:
        database = DatabaseConnection(
            host=host,
            user=user,
            password=password,
            db_name=db_name
        )

        return database.update_data(message.from_user.id)
    except Exception as exc:
        print(f'[INFO] PostgresSQL возникла ошибка во время обновления информации в базе, {exc}')
        return False
    finally:
        print('[INFO] PostgresSQL подключение обновления информации закрыто.')


# function for creating an array of chat IDs for mailing
def user_refrences_sub():
    global database  # global variable for a content database object

    try:
        database = DatabaseConnection(
            host=host,
            user=user,
            password=password,
            db_name=db_name
        )

        array = database.mailing_start()

        return array
    except Exception as exc:
        print(f'[INFO] PostgresSQL возникла ошибка во время рассылки сообщений, {exc}')
        return False
    finally:
        print('[INFO] PostgresSQL подключение рассылок закрыто.')


# reg handlers
def auth_handlers_register(dp: Dispatcher):
    dp.register_message_handler(distrib_references, commands=['reference'])
    dp.register_callback_query_handler(begin_distrib_form, text='ref_start', State=None)
    dp.register_message_handler(album_send, commands=['send', 'close'])
    dp.register_message_handler(collect_data, content_types=['photo'])
    # dp.register_message_handler(distribution, state=DistribForm.description)
