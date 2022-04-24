import pika
 
class Queue: 
    def emit(self, queue, data):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue=queue)

        channel.basic_publish(exchange='',
                            routing_key=queue,
                            body=data)
        print(data)
        connection.close()
 