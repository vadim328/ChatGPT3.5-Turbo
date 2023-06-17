import logging
import telebot
from telebot import types
import re
from settings import BOT_TOKEN
from api import generate_image, retrieve_bot_answer

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    r = bot.send_message(message.chat.id, 'Привет')
    print('#############')
    print(r)


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    how_to_button = types.KeyboardButton("Как использовать?")
    image_button = types.KeyboardButton("Сгенерировать изображение")
    markup.add(how_to_button, image_button)
    bot.send_message(message.chat.id, 'Вот тебе кнопки!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.chat.id, "Привет! \nЗадай мне свой вопрос ;)")
    elif message.text == "/help":
        bot.send_message(message.chat.id, "Напиши Привет")
    elif message.text == "Как использовать?":
        bot.send_message(message.chat.id, "Информация о возможностях")
    elif message.text == "Сгенерировать изображение" or message.text == "/img":
        context_message = bot.send_message(message.chat.id, 'Что хотите сгенерировать?')
        bot.register_next_step_handler(context_message, send_photo)
    else:
        response = retrieve_bot_answer(message.text)
        if response.status_code == 200:
            escaped_text = escape_chars(response.json()['message'])
            bot.send_message(message.from_user.id, escaped_text, parse_mode='MarkdownV2')
        else:
            bot.send_message(message.chat.id, response.json()['detail'])


def send_photo(message):
    response = generate_image(message)
    if response.status_code == 200:
        bot.send_photo(message.chat.id, response.json()['image_url'])
    else:
        bot.send_message(message.chat.id, response.json()['detail'])


def escape_chars(text):
    pattern = r"\_*[]()~>#+-=|{}.!"
    return re.sub(f"([{re.escape(pattern)}])", r"\\\1", text)


bot.infinity_polling()
