import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.token)


name = ''
surname = ''
product_id = 0
phone_number = ''

# Экран приветствия на комманду старт
# Позже этот текст помещается в описание бота и виден сразу без начала диалога


@bot.message_handler(commands=['start'])
def start(message):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    key_catalog = types.KeyboardButton(text='Каталог')
    key_create_order = types.KeyboardButton(text='Сделать заказ')
    key_get_info = types.KeyboardButton(text='Получить инфо')

    keyboard.add(key_get_info, key_create_order, key_catalog)

    msg = (f"Здравствуйте, {message.from_user.first_name}!\n"
           "Я умный бот - Тканевый Барон \n"
           "Подскажу, помогу сделать заказ :)")

    bot.send_message(message.from_user.id, msg, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text == 'Каталог':
        bot.send_message(message.from_user.id,
                         "Показываю каталог. Тут типа пачка фото.")

    elif message.text == 'Сделать заказ':
        create_order(message)

    elif message.text == 'Получить инфо':
        msg = ("Наш адрес: г.Краснодар, ул Ставропольская\n"
               "Режим работы: ПН-ЧТ 10:00-15:00\n"
               "Утренний перерыв:   11:00-12:00\n"
               "Обеденный перерыв:  13:00-14:00")
        bot.send_message(message.from_user.id, msg)

    else:
        bot.send_message(
            message.from_user.id, "Извините, не совсем Вас понял.\nПопробуйте выбрать одну из комманд :)")


def create_order(message):
    bot.send_message(message.from_user.id,
                     "Пожалуйста, напишите номер желаемой позиции :)")
    bot.register_next_step_handler(message, get_product_id)


def get_product_id(message):
    global product_id
    try:
        # проверяем, что айди введен корректно
        product_id = int(message.text)

        bot.send_message(message.from_user.id, 'Ваше имя?')
        bot.register_next_step_handler(message, get_name)
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        get_product_id(message)


def get_name(message):  # получаем имя
    # можно предложить имя пользователя из телеги или предложить ввести самому
    global name
    name = message.text
    bot.send_message(message.from_user.id,
                     'Пожалуйста, введите номер телефона')
    bot.register_next_step_handler(message, get_phone_number)


def get_phone_number(message):
    global phone_number
    phone_number = message.text
    bot.send_message(message.from_user.id,
                     'Давайте всё проверим :)')

    confirm_order(message)


def confirm_order(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура

    key_yes = types.InlineKeyboardButton(
        text='Да', callback_data='yes')
    key_no = types.InlineKeyboardButton(
        text='Нет', callback_data='no')

    keyboard.add(key_no, key_yes)

    question = (f'Ваш заказ: {product_id}\n'
                f'Ваши контактные данные:\n'
                f'{name}, т.: {phone_number}\n'
                'Всё верно?')
    bot.send_message(message.from_user.id, text=question,
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        # код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id,
                         'Передал Ваш заказ в обработку :)')
    elif call.data == "no":
        pass
        # переспрашиваем


bot.polling(none_stop=True, interval=0)

# Кароче проще заменить на клавиатурные кнопки, чем на кнопки на сообщениях.
# Так можно без калбек хандлера обрабатывать.
# Закрывать клаивиаатуру после того как сделан выбор в начале.
# Калбек хандлер использовать для подтверждения заказа.
# Посмотреть гайд с закладок
# прописать сценарии
