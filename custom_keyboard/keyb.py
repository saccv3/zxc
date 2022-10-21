from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup

phone_number_kb = ReplyKeyboardMarkup()

bt5 = KeyboardButton('Отравить свой контакт', request_contact=True)
phone_number_kb.row(bt5)

sub_menu = InlineKeyboardMarkup(row_width=1)
inl_btn = InlineKeyboardButton(text='В личные сообщения..', url='https://t.me/test_kineu_bot')

main_menu = InlineKeyboardMarkup(row_width=2)
reg_btn = InlineKeyboardButton(text='Регистрация', callback_data='reg_user')
auth_btn = InlineKeyboardButton(text='Авторизация', callback_data='auth_user')
data_btn = InlineKeyboardButton(text='Получить данные', callback_data='get_user_data')

main_menu.add(reg_btn, auth_btn).row(data_btn)
sub_menu.add(inl_btn)
