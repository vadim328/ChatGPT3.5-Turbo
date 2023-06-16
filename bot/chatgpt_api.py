import requests
from settings import GPT_TOKEN


def use_api_chatgpt(mes):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + GPT_TOKEN,
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
    print(response)
    resp_dickt = response.json()
    return resp_dickt['choices'][0]['message']['content']
