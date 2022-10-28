from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup

phone_number_kb = ReplyKeyboardMarkup()
sub_menu = InlineKeyboardMarkup(row_width=1)
auth_key_kb = InlineKeyboardMarkup(row_width=1)
main_menu = InlineKeyboardMarkup(row_width=2)

bt5 = KeyboardButton('Отравить свой контакт', request_contact=True)
phone_number_kb.row(bt5)

inl_btn = InlineKeyboardButton(text='В личные сообщения..', url='https://t.me/test_kineu_bot')
reg_btn = InlineKeyboardButton(text='Регистрация', callback_data='reg_user')
ref_btn = InlineKeyboardButton(text='Рассылка', callback_data='ref_refer')
phone_btn = InlineKeyboardButton(text='Сообщения', callback_data='message_ref')
data_btn = InlineKeyboardButton(text='Контакты', callback_data='contacts')

main_menu.add(reg_btn, data_btn)
sub_menu.add(inl_btn)
auth_key_kb.add(ref_btn, phone_btn)

# admin

admin_kb = InlineKeyboardMarkup(row_width=1).row(
    (
        InlineKeyboardButton(text='Рассылка', callback_data='ref_start')),
    InlineKeyboardButton(text='Сообщения', callback_data='message_start')
)

# accept_kb = InlineKeyboardMarkup(row_width=1).row(
#     InlineKeyboardButton(text='Отправить', callback_data='accept')
# )
