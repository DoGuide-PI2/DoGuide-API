import geocoder
import googlemaps
from geopy.geocoders import Nominatim
from datetime import datetime
from utils import rota_json
from dotenv import dotenv_values
from googlemaps import convert
import polyline
from shapely.geometry import Point
from shapely.geometry import Polygon



config = dotenv_values("../.env")

class MaaS(object):
    # self.gmaps = None
    def __init__(self):
        self.gmaps2 = googlemaps.Client(key=config['API_KEY'])

    @classmethod
    def local_partida(self):
        partida = geocoder.ip('me')
        coordenadas_partida = tuple(partida.latlng)
        # coordenadas_partida = (latitude, longitude) # Setar local de Partida caso precisão esteja equivocada
        coordenadas_partida = (-15.96108, -48.02976)

        return coordenadas_partida
    
    def destino(self, local):
        
        # local = 'Park Shopping Brasília'
        self.local = local
        destino = self.gmaps2.geocode(local)
        coordenadas_destino = (destino[0]["geometry"]["location"]['lat'], destino[0]["geometry"]["location"]['lng'])
        coordenadas_destino

        return coordenadas_destino
    
    @classmethod # API alternativa ao GoogleMaps
    def destino_alternativo(self, local):
        # local = "UnB FGA Gama"
        loc = Nominatim(user_agent="GetLoc")
        local = loc.geocode(local)
        coordenadas_destino =(local.latitude, local.longitude)

        return coordenadas_destino

    
    def instrucao_percurso(self, coordenadas_partida, coordenadas_destino):
        now = datetime.now()
        rota = self.gmaps2.directions(coordenadas_partida,coordenadas_destino,mode="walking",departure_time=now,language='pt-BR')
        rota_json(self.local, rota)
        return rota

    def gerando_segmentos_rota(self,rota):

        orientacao = {}

        pontos_rota = [poligono['polyline']['points'] for poligono in rota[0]['legs'][0]['steps']]

        pontos_polignos = []
        checkpoint = 0
        for index, elemento in enumerate(pontos_rota):
            # print(polyline.decode(elemento), rota[0]['legs'][0]['steps'][index]['html_instructions'])
            polyline_decode = polyline.decode(elemento)
            pontos_polignos+= polyline_decode

            for i in range(checkpoint, checkpoint + len(polyline_decode)): 
                orientacao[i] =  'Siga em frente' if 'maneuver' not in rota[0]['legs'][0]['steps'][index].keys() else rota[0]['legs'][0]['steps'][index]['maneuver'] 

            checkpoint += len(polyline_decode)


        return pontos_polignos, orientacao

    def gerador_polignos(self, pontos_polignos):

        par_pontos = []
        for i in range(1, len(pontos_polignos)):
            par_pontos.append([pontos_polignos[i-1], pontos_polignos[i]])

        dicionario_polignos = {}
        for index, (pontoInicial, pontoFinal) in enumerate(par_pontos):
            dicionario_polignos[index] = gerador_poligno_retangulo(pontoInicial, pontoFinal)
        
        return dicionario_polignos

    
    def checagem_rota(self, rota_poligonal, orientacao_motor, coordenada_atual):
        
        for index, poligono in enumerate(rota_poligonal.values()):
            poligono_retangulo = Polygon([poligono[0], poligono[1], poligono[2], poligono[3]])

            ponto = Point(coordenada_atual[0], coordenada_atual[1])
            if poligono_retangulo.contains(ponto):
                print(orientacao_motor[index])
            

# import json
# with open('../ultrabox_do_Gama_routes.json', 'r') as f:
#     rota = json.loads(f.read())
    # rota.close()


# instancia_rota = MaaS()

# pontos_polignos, orientacao = instancia_rota.gerando_segmentos_rota(rota)
# print(*orientacao.values(), sep='\n')

# print(pontos_polignos)
# print(len(pontos_polignos))

# resultado = instancia_rota.gerador_polignos(pontos_polignos)
# print(resultado)

# coordenada_atual = (-15.963892333916432, -48.02289801172172)
# instancia_rota.checagem_rota(resultado,orientacao, coordenada_atual)

# partida = instancia_rota.local_partida()
# local = 'UBS 5 Riacho Fundo 2' ## Definir local de Destino
# destino = instancia_rota.destino(local)
# caminho = instancia_rota.instrucao_percurso(partida, destino)

# instrucoes_percurso = instrucao_texto(caminho) # Lista de comandos para reprodução
# print(*instrucoes_percurso, sep='\n')