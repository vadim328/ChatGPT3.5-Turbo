import logging
import telebot
import telegram.constants
from telebot import types
from dotenv import dotenv_values
import requests
import re
import openai_api


env = dotenv_values(".env")
bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Как использовать?")
    item2 = types.KeyboardButton("Сгенерировать изображение")
    markup.add(item1, item2)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.chat.id, "Привет! \nЗадай мне свой вопрос ;)")
    elif message.text == "/help":
        bot.send_message(message.chat.id, "Напиши Привет")
    elif message.text == "Как использовать?":
        bot.send_message(message.chat.id, "Информация о возможностях")
    elif message.text == "Сгенерировать изображение" or message.text == "/img":
        mesg = bot.send_message(message.chat.id, 'Что хотите сгенерировать?')
        bot.register_next_step_handler(mesg, openai_api.get_image)

    else:
        msg = openai_api.use_api_chatgpt(message.text)
        escaped_text = escape_chars(msg)
        parse_mode = telegram.constants.ParseMode.MARKDOWN_V2
        bot.send_message(message.from_user.id, escaped_text, parse_mode=parse_mode)


def escape_chars(text):
    # escape_chars = r"\_*[]()~`>#+-=|{}.!"
    pattern = r"\_*[]()~>#+-=|{}.!"
    return re.sub(f"([{re.escape(pattern)}])", r"\\\1", text)


bot.infinity_polling()
#bot.polling(none_stop=True, interval=0)
