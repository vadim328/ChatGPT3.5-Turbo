import logging
import telebot
from telebot import types
import re
from settings import BOT_TOKEN
from api import get_image, send_api

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    how_to_button = types.KeyboardButton("Как использовать?")
    image_button = types.KeyboardButton("Сгенерировать изображение")
    markup.add(how_to_button, image_button)


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
        bot.register_next_step_handler(mesg, send_photo)
    else:
        resp = send_api(message.text)
        escaped_text = escape_chars(resp['message'])
        bot.send_message(message.from_user.id, escaped_text, parse_mode='MarkdownV2')


def send_photo(message):
    image_url = get_image(message)
    bot.send_photo(message.chat.id, image_url)


def escape_chars(text):
    pattern = r"\_*[]()~>#+-=|{}.!"
    return re.sub(f"([{re.escape(pattern)}])", r"\\\1", text)


bot.infinity_polling()
