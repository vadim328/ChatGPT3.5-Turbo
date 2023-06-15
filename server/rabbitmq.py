import pika
import aiormq
from termcolor import cprint
from consumer import methods
from settings import AMQP_URI
from settings import UNIQUE_PREFIX

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='my_queue')

def publish_message(message):
    channel.basic_publish(exchange='',
                          routing_key='my_queue',
                          body=message)
    print(" [x] Sent message:", message)

def consume_messages():
    def callback(ch, method, properties, body):
        print("Received message:", body)

    channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()


async def consumer_subscriptions():
    def callback(ch, method, properties, body):
        print("Received message:", body)
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()
    cprint(f"AMQP CONSUMER:     ready [yes] PREFIX={UNIQUE_PREFIX}", "green")

    # cоздадим очередь, в которую будет отправлено сообщение
    # durable значит постоянная очередь (дословный перевод прочная)
    # simple_message_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:internal__messager:test_message", durable=False)
    simple_message_queue__declared = await channel.queue_declare(f"my_queue", durable=False)
    # no_ack=True - сразу ответить брокеру что все ок, сообщение можно удалять из очереди
    await channel.basic_consume(simple_message_queue__declared.queue, on_message_callback=callback, no_ack=True)
    channel.start_consuming()


    # simple_message_with_ack_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:internal__messager:test_message_with_ack", durable=False)
    # # no_ack=False - поведение по умолчанию, отвечаем принудительно в самом обработчике по мере выполенения (предпочитаемый вариант)
    # await channel.basic_consume(simple_message_with_ack_queue__declared.queue, methods.simple_message_with_ack, no_ack=False)
    # https://habr.com/ru/post/150134/
