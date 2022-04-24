from threading import Thread
from detection.detection import detect_objects
from routes import get_route, get_directions

coordenada, destino = get_route()
t1 = Thread(target=detect_objects)
t2 = Thread(target=get_directions, args=(coordenada, destino))

t1.start()
t2.start()
t1.join()
t2.join()
