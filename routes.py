import keyboard
import time
from matplotlib.font_manager import json_dump
from pynput.keyboard import Key, Listener
import speech_recognition as sr
from google_speech import Speech
from utils import *

from MaaS.rota import MaaS
from som.audio import ModuloSom
from rabbitmq.queue import Queue

sonoplastia = ModuloSom()
maas = MaaS()
q = Queue()

def get_directions(coordenada_atual, destino):    
    sonoplastia.google_voice('Calculando Rota. Por favor, aguarde...')
    
    coordenada_destino = maas.destino(destino)
    rota = maas.instrucao_percurso(coordenada_atual, coordenada_destino)

    instrucoes, steps = instrucao_texto(rota)

    for i in range(0, len(instrucoes)):
        q.emit('control', json.dumps({
            **steps[i],
            'action': 'direction',
            'instruction': instrucoes[i]
        }))
        # print(instrucao)
        #sonoplastia.google_voice(instrucoes[i])
        time.sleep(10)


def get_route():
    coordenada_atual = maas.local_partida()

    print('Gravação Init')
    recording = sonoplastia.record(duration = 5)
    print('Gravação Encerrada')
    data_audio = sonoplastia.generate_audio(recording)

    texto = sonoplastia.transcricao_audio(data_audio)
    print('Transcrição do Áudio:', texto)
    
    destino = sonoplastia.extract_local(texto)
    time.sleep(2)

    sonoplastia.google_voice('Você deseja ir para ' + destino)
    sonoplastia.google_voice('Confirma ' + destino + ' como seu destino?????')

    if(sonoplastia.confirma_destino()):
        return coordenada_atual, destino
    else:
        sonoplastia.google_voice('refazendo o processo')
        get_route()

def exit():
        return False


# if __name__ == '__main__':
#     while True:
#         print('Pressione Enter para Gravar')
#         with Listener( on_press=main, on_release=exit) as listener:
#             listener.join()

# a, d = get_route()
# get_directions(a, d)