import logging
import telebot
import requests
import re
from settings import BOT_TOKEN
from api import get_image, send_api

bot = telebot.TeleBot(BOT_TOKEN)
logger = logging.getLogger(__name__)

# def get_image(prompt, n=1, size='512x512'):
#     url = 'https://api.openai.com/v1/images/generations'
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer ' + GPT_TOKEN,
#     }
#     data = {"prompt": prompt, "n": n, "size": size} # n - кол-во результатов
#     response = requests.post(url, headers=headers, json=data)
#     print(response)
#     img_url = response.json()['data'][0]['url']
#     return img_url


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.from_user.id, "Привет! \nЗадай мне свой вопрос ;)")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    elif message.text == "/img":
        bot.send_message(message.from_user.id, message.text)

        # url = get_image("A cute baby sea otter")
        # bot.send_photo(message.from_user.id, photo=url)
    else:
        resp = send_api(message.text)
        print(resp)
        # text = escape_chars(resp)
        bot.send_message(message.from_user.id, resp)

def escape_chars(text):
    # escape_chars = r"\_*[]()~`>#+-=|{}.!"
    pattern = r"\_*[]()~>#+-=|{}.!"
    return re.sub(f"([{re.escape(pattern)}])", r"\\\1", text)

bot.polling(none_stop=True, interval=0)

