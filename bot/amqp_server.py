import asyncio
# # from starlette.applications import Starlette
from consumer.subscriptions import consumer_subscriptions
# # from rabbitmq import consumer_subscriptions
# from fastapi import FastAPI
#
# from rabbitmq import consume_messages
#
# class AmqpHttpServer(FastAPI):
#     def __init__(self, *args, **kwargs):
#         loop = asyncio.get_event_loop()
#         loop.create_task(consumer_subscriptions())
#         super().__init__(*args, **kwargs)
#
#
# app = AmqpHttpServer()
#

# import uvicorn


# from fastapi import FastAPI
# # from consumer.subscriptions import mq, connect_to_broker
#
#
# app = FastAPI()
#
#
# @app.on_event('startup')
# async def start_message_consuming():
#     channel = await connect_to_broker()
#     mq.channel = channel
#     await mq.consume_queue(mq_accept_message, "mq_test_queue")
#
# async def mq_accept_message(msg) -> None:
#     """MQ-функция которая слушает очередь test-queue приходит объект IncomingMessage"""
#     print('BOT CONSUMER')
#     # test = 1 / 0
#     # Если не ack-ать message тогда она будет висеть в рабите
#     # и при перезапуске приложения этот message снова попадет в функцию.
#     await msg.ack()

def main():
    loop = asyncio.get_event_loop()
    loop.create_task(consumer_subscriptions())


if __name__ == "__main__":
    main()
