import telebot
from telebot import types
import re
from settings import BOT_TOKEN
from api import generate_image, retrieve_bot_answer

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Напиши /button')


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    how_to_button = types.KeyboardButton("Инфо")
    image_button = types.KeyboardButton("DALLE")
    info_button = types.KeyboardButton("Кто мы?")
    markup.add(how_to_button, image_button, info_button)
    bot.send_message(message.chat.id, 'Вот тебе кнопки!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.chat.id, "Привет! \nЗадай мне свой вопрос ;)")
    elif message.text == "/help":
        bot.send_message(message.chat.id, "Напиши /button")
    elif message.text == "Инфо.":
        bot.send_message(message.chat.id, "Информация о боте:\n"
                                          "Бот построен на основе языковой модели OpenAI GPT-3.5 Turbo, "
                                          "созданной для выполнения различных задач обработки естественного языка.\n"
                                          "Также данный бот свособен генерировать изображения "
                                          "с помощью нейронной сети DALLE.\n"
                                          "Для общения с ботом просто начни писать. "
                                          "Для генерации изображений нажми на кнопку 'Сгенерировать изображение'"
                                          "или напиши /img.")
    elif message.text == "Кто мы?":
        bot.send_message(message.chat.id, "Мы команда разработчиков Уральского федерального университета."
                                          "Наш GitHub: https://github.com/vadim328/ChatGPT3.5-Turbo")
    elif message.text == "DALLE" or message.text == "/img":
        context_message = bot.send_message(message.chat.id,
                                           'Что хотите сгенерировать?')
        bot.register_next_step_handler(context_message, count_image)
    else:
        response = retrieve_bot_answer(message.text)
        if response.status_code == 200:
            escaped_text = escape_chars(response.json()['message'])
            bot.send_message(message.from_user.id,
                             escaped_text,
                             parse_mode='MarkdownV2')
        else:
            bot.send_message(message.chat.id, response.json()['detail'])


def send_photo(message, img_prompt):
    response = generate_image(message, img_prompt)
    if response.status_code == 200:
        for image in response.json()['image_urls']:
            bot.send_photo(message.chat.id, image['url'])
    else:
        bot.send_message(message.chat.id, response.json()['detail'])


def escape_chars(text):
    pattern = r"\_*[]()~>#+-=|{}.!"
    return re.sub(f"([{re.escape(pattern)}])", r"\\\1", text)


def count_image(message):
    count_img = bot.send_message(message.chat.id, 'Введите количество изображений')
    bot.register_next_step_handler(count_img, send_photo, message.text)


bot.infinity_polling()
