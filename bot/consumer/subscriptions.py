# # import asyncio
# import logging
#
# import os
# # import copy
# import json
# from typing import Any
# from uuid import uuid4
# from time import sleep
#
# import aio_pika
# from functools import partial
# from aio_pika.channel import Channel
# from aio_pika.message import IncomingMessage, Message
#
# RMQ_LOGIN = os.environ.get("RMQ_LOGIN", "guest")
# RMQ_PASSWORD = os.environ.get("RMQ_PASSWORD", "guest")
# RMQ_HOST = os.environ.get("RMQ_HOST", "rabbitmq")
# RMQ_PORT = os.environ.get("RMQ_PORT", "5672")
#
# # Эти глобальные переменные хранят объекты соединения и канала к брокеру.
# # Функция connect_to_broker пытается в первую очередь использовать их, но если их нет, то она создаст их.
# BROKER_CONNECTION = None
# BROKER_CHANNEL = None
#
#
# class BaseRMQ:
#
#     channel = None
#
#     def __init__(self, channel: Channel = None):
#         self.channel = channel
#
#     @staticmethod
#     def serialize(data: Any) -> bytes:
#         return json.dumps(data).encode()
#
#     @staticmethod
#     def deserialize(data: bytes) -> Any:
#         return json.loads(data)
#
#
# class MessageQueue(BaseRMQ):
#     async def send(self, queue_name: str, data: Any):
#         message = Message(
#             body=self.serialize(data),
#             content_type="application/json",
#             correlation_id=str(uuid4()),
#         )
#         await self.channel.default_exchange.publish(message, queue_name)
#
#     async def consume_queue(self, func, queue_name: str, auto_delete_queue: bool = False):
#         queue = await self.channel.declare_queue(queue_name, auto_delete=auto_delete_queue, durable=True)
#         async with queue.iterator() as queue_iter:
#             async for message in queue_iter:
#                 logging.debug(f'Received message body: {message.body}')
#                 await func(message)
#
#
# async def connect_to_broker() -> Channel:
#     global BROKER_CONNECTION
#     global BROKER_CHANNEL
#
#     retries = 0
#     while not BROKER_CONNECTION:
#         conn_str = f"amqp://{RMQ_LOGIN}:{RMQ_PASSWORD}@{RMQ_HOST}:{RMQ_PORT}/"
#         print(f"Trying to create connection to broker: {conn_str}")
#         try:
#             BROKER_CONNECTION = await aio_pika.connect_robust(conn_str)
#             print(f"Connected to broker ({type(BROKER_CONNECTION)} ID {id(BROKER_CONNECTION)})")
#         except Exception as e:
#             retries += 1
#             print(f"Can't connect to broker {retries} time({e.__class__.__name__}:{e}). Will retry in 5 seconds...")
#             sleep(5)
#
#     if not BROKER_CHANNEL:
#         print("Trying to create channel to broker")
#         BROKER_CHANNEL = await BROKER_CONNECTION.channel()
#         print("Got a channel to broker")
#
#     return BROKER_CHANNEL
#
#
# mq = MessageQueue()

import aiormq
from termcolor import cprint

from consumer import methods
from settings import AMQP_URI
from settings import UNIQUE_PREFIX


async def consumer_subscriptions():
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()

    cprint(f"AMQP CONSUMER:     ready [yes] PREFIX={UNIQUE_PREFIX}", "green")

    # cоздадим очередь, в которую будет отправлено сообщение
    # durable значит постоянная очередь (дословный перевод прочная)
    simple_message_queue__declared = await channel.queue_declare("internal_messager", durable=False)

    # no_ack=True - сразу ответить брокеру что все ок, сообщение можно удалять из очереди
    await channel.basic_consume(simple_message_queue__declared.queue, methods.simple_message, no_ack=True)

    simple_message_with_ack_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:internal__messager:test_message_with_ack", durable=False)
    await channel.basic_consume(simple_message_with_ack_queue__declared.queue, methods.simple_message_with_ack, no_ack=False)

    # chat_message_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:internal__messager:chat_message",
    #                                                            durable=False)
    # await channel.basic_consume(chat_message_queue__declared.queue, methods.chat_message, no_ack=False)
