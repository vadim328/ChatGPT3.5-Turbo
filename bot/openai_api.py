import requests
import telebot
from dotenv import dotenv_values

env = dotenv_values(".env")
bot = telebot.TeleBot('TOKEN')
APIKEY = 'APIKEY'


def use_api_chatgpt(mes):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + APIKEY,
    }

    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'user',
                'content': mes,
            },
        ],
        'temperature': 0.7,
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
    resp_dickt = response.json()
    return resp_dickt['choices'][0]['message']['content']


def get_image(message):
    url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + APIKEY,
    }
    data = {"prompt": message.text, "n": 2, "size": "512x512"} # n - кол-во результатов
    response = requests.post(url, headers=headers, json=data)
    img_url = response.json()['data'][0]['url']
    bot.send_photo(message.chat.id, img_url)
