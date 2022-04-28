from ast import If
from xml.sax.handler import feature_external_ges
import telebot
from telebot import types
token = '5398802223:AAFtbdoX_tZtHn36sRVf8pl7lgg1sMzh4hw'
bot = telebot.TeleBot(token)


name = ''
surname = ''
age = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id,
                     f'Здравствуйте, {message.from_user.first_name}!\nЯ умный бот - Тканевый Барон \nПодскажу, помогу сделать заказ :)')

    keyboard = types.KeyboardMarkup()  # наша клавиатура

    key_catalog = types.InlineKeyboardButton(
        text='Каталог', callback_data='catalog')  # кнопка «Каталог»
    keyboard.add(key_catalog)  # добавляем кнопку в клавиатуру

    key_create_order = types.InlineKeyboardButton(
        text='Сделать заказ', callback_data='create_order')
    keyboard.add(key_create_order)

    key_get_info = types.InlineKeyboardButton(
        text='Получить инфо', callback_data='get_info')
    keyboard.add(key_get_info)

    bot.send_message(message.from_user.id,
                     text='Выберите действие', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def forReg(message):

    # if message.text == '/reg':  # Тут все синонимы слова заказ
    bot.send_message(message.from_user.id, "Как тебя зовут?")
    # следующий шаг – функция get_name
    bot.register_next_step_handler(message, get_name)
    # else:
    # bot.send_message(message.from_user.id, 'Напиши /reg')


def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    try:
        age = int(message.text)  # проверяем, что возраст введен корректно
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')

    keyboard = types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура

    key_yes = types.InlineKeyboardButton(
        text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру

    key_no = types.InlineKeyboardButton(
        text='Нет', callback_data='no')
    keyboard.add(key_no)

    question = f'Тебе {age} лет, тебя зовут {name} {surname}?'
    bot.send_message(message.from_user.id, text=question,
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        pass
        # код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Запомню :)')
    elif call.data == "no":
        pass
        # переспрашиваем
    elif call.data == "catalog":
        bot.send_message(call.message.chat.id, 'Это каталог')
        pass
    elif call.data == "create_order":
        bot.send_message(call.message.chat.id, 'Сейчас оформим заказ')
        forReg(call.message)
        pass
    elif call.data == "get_info":
        bot.send_message(call.message.chat.id, 'Это информация')
        pass


bot.polling(none_stop=True, interval=0)

# Кароче проще заменить на клавиатурные кнопки, чем на кнопки на сообщениях.
# Так можно без калбек хандлера обрабатывать.
# Посмотреть гайд с закладок
# прописать сценарии
