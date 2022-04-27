import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import speech_recognition as sr
from google_speech import Speech
import keyboard
import os
from collections import defaultdict
from tqdm import tqdm



class ModuloSom(object):

    def __init__(self):
        self.dicionario_palavras= { 'eu':True, 'gostaria':True, 'de':True, 'ir':True, 'para':True,
        'favor':True, 'ir':True, 'leve':True, 'me':True, 'mim':True, 'leve-me':True,
        'desejo':True, 'por favor':True, 'por':True, 'quero':True, 'leva':True,
        'daqui':True, 'onde':True, 'estou':True, 'pra':True, 'sair': True,
        'o':True, 'a':True,'e':True,'i':True,'u':True, 'doguide':True, 'dogaide':True, 'dog':True, 'Dog': True
        }

        self.dicionario_positivo = {
            'sim':True, 'ok':True, 'isso':True, 'confirmado':True, 'verdade':True, 'beleza':True, 'okay':True, 'yes':True, 'Sim': True
        }

        self.r = sr.Recognizer()
        self.temp = 'temp/'        
    def extract_local(self, recorded_voice):
        local = []
        for palavra in recorded_voice.split():
            if(palavra.lower() not in self.dicionario_palavras):
                local.append(palavra)    
        return ' '.join(local)

    def google_voice(self, frase):
        lang = "pt"
        speech = Speech(frase, lang)
        speech.play()

    def record(self, freq = 44100,  duration = 3):
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
        sd.wait()

        return recording

    def generate_audio(self, recording, freq=44100):
        
        if not os.path.exists(self.temp): os.makedirs(self.temp)

        wv.write(self.temp + "temp_audio.wav", recording, freq, sampwidth=2)
        load_audio = sr.AudioFile(self.temp + 'temp_audio.wav')
        with load_audio as source:
            data_audio = self.r.record(source)

        return data_audio

    def transcricao_audio(self, data_audio):
        return self.r.recognize_google(data_audio, language = 'pt-PT')


    def confirma_destino(self):
        # google_voice('')
        try:
            print('Gravar Resposta')
            recording = self.record(duration = 5)
            data_audio = self.generate_audio(recording)
            print('Resposta:', self.transcricao_audio(data_audio))
            print('Gravação Encerrada')
            
            texto = self.r.recognize_google(data_audio, language = 'pt-PT')
            for confirmacao in texto.lower().split():
                if confirmacao in self.dicionario_positivo:
                    # google_voice(texto)
                    return True
        except Exception as e:
            print(e)
            return False
        

