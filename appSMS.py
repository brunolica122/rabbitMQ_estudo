import os
import pika
from twilio.rest import Client


RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'admin'
RABBITMQ_PASSWORD = 'admin'
RABBITMQ_QUEUE = 'files_modificados'


TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_FROM_NUMBER = ''
TO_PHONE_NUMBER = ''

class MyConsumer:
    def __init__(self):
        self.connection = None

    def connect(self):
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=RABBITMQ_QUEUE)

    def consume(self, ch, method, properties, body):
        message = body.decode()
        print(f"Recebido do RabbitMQ: {message}")
        self.send_sms(message)

    def start_consuming(self):
        self.channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=self.consume, auto_ack=True)
        self.channel.start_consuming()

    def send_sms(self, message):
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(body=message, from_=TWILIO_FROM_NUMBER, to=TO_PHONE_NUMBER)
            print(f"Mensagem enviada para o número {TO_PHONE_NUMBER} com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar mensagem para o número {TO_PHONE_NUMBER}: {e}")

if __name__ == "__main__":
    consumer = MyConsumer()
    consumer.connect()
    consumer.start_consuming()
