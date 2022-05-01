import json
import pika
from som.audio import ModuloSom

sonoplastia = ModuloSom()

class Blackboard:
    def __init__(self) -> None:
        self.queue = 'control'
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        self.check_obstacle = False
        self.directions = []


    def callback(self, ch, method, properties, body):
        self.send_action_to_actuators(json.loads(body))
        #time.sleep(randrange(0, 5))
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def send_action_to_actuators(self, body):
        action = body['action']

        if action == 'detection':
            print('DETECTION: Objeto "{}" detectado'.format(body['name']))
            if self.check_obstacle is False:
                sonoplastia.google_voice('Objeto "{}" detectado em frente ao robô. Atenção.'.format(body['name']))
                self.check_obstacle = True

        elif action == 'direction':
            self.directions.append(body['instruction'])
        
        elif action == 'no_detection':
            if len(self.directions) > 0:
                direction = self.directions.pop(0)
                print('DIRECTION: ' + direction)
                sonoplastia.google_voice(direction)
                self.check_obstacle = False            
            
    def run(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(on_message_callback=self.callback,
                            queue=self.queue)

        self.channel.start_consuming()

blackboard = Blackboard()

blackboard.run()
