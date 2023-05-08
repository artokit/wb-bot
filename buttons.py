from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def phone_number_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    phone_number_btn = KeyboardButton('Отправить номер телефона', request_contact=True)

    kb.add(phone_number_btn)

    return kb


def pdf_inline_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Топ 10 товаров на ВБ", callback_data="cb_pdf"))

    return markup


def inline_pages(current_page):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('Пред.', callback_data=f'page:{current_page-1}'),
        InlineKeyboardButton('Cлед.', callback_data=f'page:{current_page+1}')
    )
    return keyboard
