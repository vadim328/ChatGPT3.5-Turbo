import requests
from dotenv import dotenv_values

env = dotenv_values(".env")


def use_api_chatgpt(mes):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer OPENAI_API_KEY',
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