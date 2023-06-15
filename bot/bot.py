import logging
import telebot
import chatgpt_api
from dotenv import dotenv_values
import requests

env = dotenv_values(".env")

bot = telebot.TeleBot('TOKEN')


def get_image(prompt):
    url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer OPENAI_API_KEY',
    }
    data = {"prompt": prompt, "n": 2, "size": "512x512"} # n - кол-во результатов
    response = requests.post(url, headers=headers, json=data)
    img_url = response.json()['data'][0]['url']
    return img_url


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.from_user.id, "Привет! \nЗадай мне свой вопрос ;)")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    elif message.text == "/img":
        url = get_image("A cute baby sea otter")
        bot.send_photo(message.from_user.id, photo=url)
    else:
        bot.send_message(message.from_user.id, chatgpt_api.use_api_chatgpt(message.text))


bot.polling(none_stop=True, interval=0)

