import os
import time
import pika
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'admin'
RABBITMQ_PASSWORD = 'admin'
RABBITMQ_QUEUE = 'files_modificados'

class MyHandler(FileSystemEventHandler):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def on_any_event(self, event):
        if event.is_directory:
            return
        elif event.event_type == 'created':
            self.send_message(f"Arquivo criado: {event.src_path}")
        elif event.event_type == 'deleted':
            self.send_message(f"Arquivo deletado: {event.src_path}")
        elif event.event_type == 'modified':
            self.send_message(f"Arquivo modificado: {event.src_path}")

    def send_message(self, message):
        try:
            channel = self.connection.channel()
            channel.queue_declare(queue=RABBITMQ_QUEUE)
            channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=message)
            print(f"Mensagem enviada para o RabbitMQ: {message}")
        except Exception as e:
            print(f"Erro ao enviar mensagem para o RabbitMQ: {e}")

if __name__ == "__main__":
 
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)))
        print("Conexão com o RabbitMQ estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao RabbitMQ: {e}")
        exit()

    path = "/home/arquivos_secretos"

    event_handler = MyHandler(connection)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Monitorando o diretório: {path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
