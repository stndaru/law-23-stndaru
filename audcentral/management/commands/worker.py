from django.core.management.base import BaseCommand
from .acFunctions import *
import pika, os, sys

class Command(BaseCommand):
    def handle(self, **options):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()

            channel.queue_declare(queue='test0')

            def callback(ch, method, properties, body):
                print(randomSongJSON())

            channel.basic_consume(queue='test0', on_message_callback=callback, auto_ack=True)

            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
