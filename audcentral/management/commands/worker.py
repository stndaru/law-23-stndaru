from django.core.management.base import BaseCommand
from ...acfunctions.RandomSong import *
from ...acfunctions.TranscribeText import *
import pika, os, sys

class Command(BaseCommand):
    def handle(self, **options):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()

            channel.queue_declare(queue='transcribe0')

            def callback(ch, method, properties, body):
                message = json.loads(body)
                if message["task"] == "transcribe":
                    try:
                        ID = str(message["obj_id"])
                        print(f"Start transcribing data for ID {ID}...")
                        context = transcribeTextData(None, message["audio_info"], None, message["obj_id"], message["storage_id"])
                    except:
                        transcribed_audio_obj = TranscriptResult.objects.get(pk=message["obj_id"])
                        transcribed_audio_obj.status = "Error"
                        transcribed_audio_obj.status_description = "Error processing the file"
                        transcribed_audio_obj.save()

            channel.basic_consume(queue='transcribe0', on_message_callback=callback, auto_ack=True)

            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
