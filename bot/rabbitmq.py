# import pika
# import aiormq
# from termcolor import cprint
# # from consumer import methods
# from settings import AMQP_URI
# from settings import UNIQUE_PREFIX
# credentials = pika.PlainCredentials('guest', 'guest')
# parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
# connection = pika.BlockingConnection(parameters)
# channel = connection.channel()
#
# channel.queue_declare(queue='mq_test_queue', durable=True)
#
#
# def publish_message(message):
#     channel.basic_publish(exchange='', routing_key='mq_test_queue', body=message)
#     print(" [x] Sent message:", message)
#
#
# def consume_messages():
#     def callback(ch, method, properties, body):
#         print("Received message:", body)
#
#     channel.queue_declare("mq_test_queue2", durable=True)
#     channel.basic_consume('mq_test_queue2', on_message_callback=callback, auto_ack=True)
#     # channel.basic_consume(queue='mq_test_queue', on_message_callback=callback, auto_ack=True)
#     print('Waiting for messages. To exit press CTRL+C')
#
#     channel.start_consuming()

# async def consumer_subscriptions():
#     def callback(ch, method, properties, body):
#         print("Received message:", body)
#     connection = await aiormq.connect(AMQP_URI)
#     channel = await connection.channel()
#     cprint(f"AMQP CONSUMER:     ready [yes] PREFIX={UNIQUE_PREFIX}", "green")
#
#     # cоздадим очередь, в которую будет отправлено сообщение
#     # durable значит постоянная очередь (дословный перевод прочная)
#     # simple_message_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:internal__messager:test_message", durable=False)
#     simple_message_queue__declared = await channel.queue_declare("mq_test_queue", durable=False)
#     # no_ack=True - сразу ответить брокеру что все ок, сообщение можно удалять из очереди
#     await channel.basic_consume(simple_message_queue__declared.queue, on_message_callback=callback, no_ack=True)
#     channel.start_consuming()


# simple_message_with_ack_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:internal__messager:test_message_with_ack", durable=False)
# # no_ack=False - поведение по умолчанию, отвечаем принудительно в самом обработчике по мере выполенения (предпочитаемый вариант)
# await channel.basic_consume(simple_message_with_ack_queue__declared.queue, methods.simple_message_with_ack, no_ack=False)
# https://habr.com/ru/post/150134/

import aiormq
from termcolor import cprint

# from consumer import methods
from settings import AMQP_URI
from settings import UNIQUE_PREFIX

async def simple_message(message):
    print("simple_message :: Simple message body is: %r" % message.body)


async def simple_message_with_ack(message):
    print("simple_message_with_ack :: Simple message body is: %r" % message.body)
    await message.channel.basic_ack(message.delivery.delivery_tag)

async def consumer_subscriptions():
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()

    cprint(f"AMQP CONSUMER:     ready [yes] PREFIX={UNIQUE_PREFIX}", "green")

    # cоздадим очередь, в которую будет отправлено сообщение
    # durable значит постоянная очередь (дословный перевод прочная)
    simple_message_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:internal__messager:test_message",
                                                                 durable=False)

    # no_ack=True - сразу ответить брокеру что все ок, сообщение можно удалять из очереди
    await channel.basic_consume(simple_message_queue__declared.queue, simple_message, no_ack=True)

    simple_message_with_ack_queue__declared = await channel.queue_declare(
        f"{UNIQUE_PREFIX}:internal__messager:test_message_with_ack", durable=False)
    await channel.basic_consume(simple_message_with_ack_queue__declared.queue, simple_message_with_ack,
                                no_ack=False)

    chat_message_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:internal__messager:chat_message",
                                                               durable=False)
    await channel.basic_consume(chat_message_queue__declared.queue, methods.chat_message, no_ack=False)
