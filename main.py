import telebot
from telebot.types import Message, CallbackQuery
import buttons
import database
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('6229198848:AAHBzPJ2O-TgZv4zt9bGSsMHlAEXnFNtow0')
# bot = telebot.TeleBot('6122853784:AAFicZRlkquME4SOM4N34Sxg2PwXorR8zK8')
ADMINS = [482010517, 6001909175]
print(bot.get_me())


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    ref = message.text.split(' ', maxsplit=1)[-1]
    database.pre_register_user(user_id, ref if ref != '/start' else None)

    main_text = 'Что бы завершить регистрацию на интенсив «Продвижение на WB без самовыкупов», оставь свой номер. ' \
                'Обещаю ни какого спама, только напоминания о встрече. Нажми на кнопку ниже, что бы поделиться ' \
                'номером Регистрация через бота (сбор телофон) текст кнопки: зарегестрироваться на 3х дневный ' \
                'интенсив «Продвижение на WB без самовыкупов».'

    bot.send_message(user_id, 'Поздравляем первый шаг к миллиону на WB сделан!')
    bot.send_message(user_id, main_text, reply_markup=buttons.phone_number_button())

    bot.register_next_step_handler(message, get_number)


def get_number(message: Message):
    user_id = message.from_user.id

    if message.contact:
        phone_number = message.contact.phone_number
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Подписаться на канал', url='https://t.me/snaimanawb'))

        # checker = database.check_user(phone_number)

        # if checker:
        #     bot.send_message(user_id, 'Спасибо за регистрацию на 3х дневный интенсив!',
        #                                reply_markup=buttons.pdf_inline_button())

        # else:
        database.register_user(message.chat.id, phone_number)
        bot.send_message(user_id, 'Спасибо за регистрацию на 3х дневный интенсив!',
                         reply_markup=buttons.pdf_inline_button())

        bot.send_message(user_id, 'Я предпочитаю действовать, а не ждать!', reply_markup=markup)

    else:
        bot.send_message(user_id, 'Отправьте номер используя кнопку ниже')
        bot.register_next_step_handler(message, get_number)


@bot.callback_query_handler(func=lambda call: call.data.startswith('page'))
def get_pages(call: CallbackQuery):
    page = int(call.data.split(':')[1])
    users = get_users_page(page)
    text = ''
    for user in users:
        url = f'<a href="tg://user?id={user[0]}">User №{user[0]}</a>'
        channel = f'Канал: <a href="https://t.me/{user[3]}">{user[3]}</a>' if user[3] else ''
        text += f'{url}\nНомер: {user[1]}\n{channel}\n\n'

    if text != '':
        bot.edit_message_text(
            text, call.message.chat.id, call.message.id, parse_mode='html', reply_markup=buttons.inline_pages(page)
        )
    else:
        bot.send_message(call.message.chat.id, 'Cтраница пустая!')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_pdf":
        # doc = open('documents/ТОП 10 товар на вайлтберис.pdf', 'rb') # Отправка файла (файл не должен быть слишком большим)
        # bot.send_document(call.from_user.id, doc)
        bot.send_message(call.from_user.id, 'https://disk.yandex.ru/i/bdufZN0q2Ow3SA')


@bot.message_handler(commands=['create_ref'])
def create_ref(message: Message):
    if message.chat.id in ADMINS:
        bot.send_message(message.chat.id, 'Cкиньте собачку канала')
        bot.register_next_step_handler(message, enter_name_for_url)


def enter_name_for_url(message: Message):
    if message.text.startswith('@'):
        bot.send_message(
            message.chat.id,
            f'Используйте данную ссылку для рефералки: https://t.me/bestinessa_pezzolini_bot?start={message.text[1:]}',
        )
    else:
        bot.send_message(
            message.chat.id,
            f'Cкиньте собачку канала (начинается с @)'
        )
        bot.register_next_step_handler(message, enter_name_for_url)


@bot.message_handler(commands=['send'])
def send_step(message: Message):
    if message.chat.id in ADMINS:
        bot.send_message(message.chat.id, 'Что бы вы хотели отправить ?')
        bot.register_next_step_handler(message, send_all)


def send_all(message: Message):
    if message.photo:
        f, kwargs = bot.send_photo, {'photo': message.photo[-1].file_id, 'caption': message.caption}

    else:
        f, kwargs = bot.send_message, {'text': message.text}

    for user_id in database.get_users_id():
        try:
            f(chat_id=user_id[0], **kwargs)
        except Exception as e:
            print(str(e))


@bot.message_handler(commands=['get_list'])
def get_user_list(message: Message):
    if message.chat.id in ADMINS:
        users = get_users_page(1)
        text = ''
        for user in users:
            url = f'<a href="tg://user?id={user[0]}">User №{user[0]}</a>'
            channel = f'Канал: <a href="https://t.me/{user[3]}">{user[3]}</a>' if user[3] else ''
            text += f'{url}\nНомер: {user[1]}\n{channel}\n\n'
        bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=buttons.inline_pages(1))


def get_users_page(page):
    page -= 1
    num = 5
    return database.get_users()[page*num:(page+1)*num]


while True:
    try:
        bot.polling()
    except Exception as exc:
        print(str(exc))
