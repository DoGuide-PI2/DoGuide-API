import keyboard
import time
from pynput.keyboard import Key, Listener
import speech_recognition as sr
from google_speech import Speech
from utils import *

from MaaS.rota import MaaS
from som.audio import ModuloSom


def main(key):
    sonoplastia = ModuloSom()
    maas = MaaS()
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
        sonoplastia.google_voice('Calculando Rota. Por favor, aguarde...')
        
        coordenada_destino = maas.destino(destino)
        rota = maas.instrucao_percurso(coordenada_atual, coordenada_destino)
        
        
        for instrucao in instrucao_texto(rota):
            # print(instrucao)
            sonoplastia.google_voice(instrucao)
            time.sleep(5)

    else:
        sonoplastia.google_voice('refazendo o processo')

def exit(key):
        return False    


if __name__ == '__main__':
    while True:
        print('Pressione Enter para Gravar')
        with Listener( on_press=main, on_release=exit) as listener:
            listener.join()
        