import json
import pika
import time
from random import randrange

class Blackboard:
    def __init__(self) -> None:
        self.queue = 'control'
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)


    def callback(self, ch, method, properties, body):
        self.send_action_to_actuators(json.loads(body))
        #time.sleep(randrange(0, 5))
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def send_action_to_actuators(self, body):
        action = body['action']

        if action == 'detection':
            print('DETECTION: Objeto "{}" detectado em frente ao robô, desvie do objeto de acordo as definições enviadas'.format(body['name']))
        elif action == 'direction':
            print('DIRECTION: ' + body['instruction'])
            
    def run(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(on_message_callback=self.callback,
                            queue=self.queue)

        self.channel.start_consuming()

blackboard = Blackboard()

blackboard.run()
