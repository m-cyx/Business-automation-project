import telebot
token = '5398802223:AAFtbdoX_tZtHn36sRVf8pl7lgg1sMzh4hw'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name}, вы хотите купить ткань?'
    bot.send_message(message.from_user.id, mess)



@bot.message_handler(content_types=['text'])
def get_user_text(message):

    if message.text == "Привет":
        mess = f'Привет, {message.from_user.first_name}, вы хотите купить тттт ткань?'
        bot.send_message(message.from_user.id, mess)
    




bot.polling(none_stop=True, interval=0)
