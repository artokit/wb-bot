import telebot
from telebot.types import Message, ReplyKeyboardRemove
import buttons
import database
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('6229198848:AAHBzPJ2O-TgZv4zt9bGSsMHlAEXnFNtow0')
# bot = telebot.TeleBot('5450270265:AAF-jeIKwLYON-yLWnrBUxv-v5d1ru0uchg')
ADMINS = [482010517]


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id

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

        checker = database.check_user(phone_number)

        if checker:
            bot.send_message(user_id, 'Спасибо за регистрацию на 3х дневный интенсив!',
                                       reply_markup=buttons.pdf_inline_button())

        else:
            database.register_user(message.chat.id, phone_number)
            bot.send_message(user_id, 'Спасибо за регистрацию на 3х дневный интенсив!',
                                       reply_markup=buttons.pdf_inline_button())

        bot.send_message(user_id, 'Я предпочитаю действовать, а не ждать!', reply_markup=markup)

    else:
        bot.send_message(user_id, 'Отправьте номер используя кнопку ниже')
        bot.register_next_step_handler(message, get_number)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_pdf":
        # doc = open('documents/ТОП 10 товар на вайлтберис.pdf', 'rb') # Отправка файла (файл не должен быть слишком большим)
        # bot.send_document(call.from_user.id, doc)
        bot.send_message(call.from_user.id, 'https://disk.yandex.ru/i/bdufZN0q2Ow3SA')


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


bot.polling()
