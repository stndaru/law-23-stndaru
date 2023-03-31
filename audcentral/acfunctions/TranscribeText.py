import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='test0')

channel.basic_publish(exchange='', routing_key='test0', body='Hello World!')
print(" [x] Sent call")
connection.close()