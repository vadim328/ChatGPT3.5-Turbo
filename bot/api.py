import requests
from settings import SERVER_URL, FASTAPI_ACCESS_TOKEN


def get_image(params):
    url = SERVER_URL + '/image'
    headers = {"Content-Type": "application/json"}
    data = {"token": "123", "message": params}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['image_url']


def send_api(message):
    url = SERVER_URL + '/bot'
    headers = {"Content-Type": "application/json"}
    data = {"token": "123", "messages": message}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
