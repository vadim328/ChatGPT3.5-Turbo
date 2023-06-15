from fastapi import FastAPI, Body
import requests
import asyncio
# from starlette.applications import Starlette
# from consumer.subscriptions import consumer_subscriptions
# from rabbitmq import publish_message
from consumer.subscriptions import mq, connect_to_broker

# class AmqpHttpServer(Starlette):
#     def __init__(self, *args, **kwargs):
#         loop = asyncio.get_event_loop()
#         loop.create_task(consumer_subscriptions())
#         super().__init__(*args, **kwargs)
#
#
# app = AmqpHttpServer(debug=True)
from settings import GPT_TOKEN, GPT_URL

app = FastAPI()

@app.on_event('startup')
async def start_message_consuming():
    channel = await connect_to_broker()
    mq.channel = channel

    await mq.consume_queue(mq_accept_message, "mq_test_queue")

async def mq_accept_message(msg) -> None:
    """MQ-функция которая слушает очередь test-queue приходит объект IncomingMessage"""
    print('HEEEEEEEEEEEEEEEEEEEEEELLLLOOOOOOOOOOOOOOO WORL!')
    # test = 1 / 0
    # Если не ack-ать message тогда она будет висеть в рабите
    # и при перезапуске приложения этот message снова попадет в функцию.
    await msg.ack()


@app.get("/")
async def root():
    # publish_message("Hello from FastAPI!")
    return {"message": "Hello World rabbitmq"}


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
    headers = {"Authorization": "Bearer " + GPT_TOKEN, "Content-Type": "application/json"}
    data = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(GPT_URL, headers=headers, json=data)
    print(response.json())
    return response.json()['choices'][0]['message']['content']


# возвращает ссылку на изображение, нужно сделать скачиватель изображения и отправщик в тг-бот
def get_image(prompt):
    url = 'https://api.openai.com/v1/images/generations'
    headers = {"Authorization": "Bearer " + GPT_TOKEN, "Content-Type": "application/json"}
    data = {"prompt": prompt, "n": 2, "size": "1024x1024"} # n - кол-во результатов
    response = requests.post(url, headers=headers, json=data)
    return response.json()
