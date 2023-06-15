from fastapi import FastAPI, Body
from dotenv import dotenv_values
import requests


env = dotenv_values(".env")
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/bot")
async def bot(data: str = Body()):
    print(data)
    resp = send_request(data)
    return {"message": resp}


@app.get("/hello")
async def hello():
    return {"message": 'Hello!!!!'}


@app.post("/image")
async def image():
    resp = get_image('A cute baby sea otter wearing a beret')
    return {"message": resp}


def send_request(prompt, model="gpt-3.5-turbo", max_tokens=60):
    url = env['GPT_URL']
    headers = {
        "Authorization": "Bearer " + env["GPT_TOKEN"],
        "Content-Type": "application/json"
    }
    data = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    return response.json()['choices'][0]['message']['content']


# возвращает ссылку на изображение, нужно сделать скачиватель изображения и отправщик в тг-бот
def get_image(prompt):
    url = 'https://api.openai.com/v1/images/generations'
    headers = {
        "Authorization": "Bearer " + env["GPT_TOKEN"],
        "Content-Type": "application/json"
    }
    data = {"prompt": prompt, "n": 2, "size": "512x512"} # n - кол-во результатов
    response = requests.post(url, headers=headers, json=data)
    return response.json()
