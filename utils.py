import re
import json

def clean(string):
    string = str(string)
    string = re.sub(r"\n", ".", string)
    string = re.sub(r"\r", "", string)
    string = re.sub(r"\'", "", string)
    string = re.sub(r"\"", "", string)
    string = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[]^_`{|}~"""), ' ', string)
    string = string.replace('\x0c', '')
    string = string.replace('º', '')
    string = string.replace('nº', '')
    string = string.replace('ii ', '2')
    string = string.replace('qs', 'Quadra Sul')
    string = string.replace('sqs', ' Super Quadra Sul ')
    string = string.replace('sqn', ' Super Quadra Norte ')
    string = string.replace('sqsw', ' Super Quadra Sudoeste ')
    string = string.replace('sqnw', ' Super Quadra Noroeste ')
    string = string.replace('cls', ' Comércio Local Sul ')
    string = string.replace('cln', ' Comércio Local Norte ')
    string = string.replace('clsw', ' Comércio Local Sudoeste ')
    string = string.replace('clnw', ' Comércio Local Noroeste ')
    string = string.replace('road', 'Avenida')
    string = string.replace('estrada de uso restrito', '')
    string = string.replace('&nbsp', '')
    string = string.replace('nbsp', '')

    return string

def cleanhtml(raw_html):
    CLEANR = re.compile('<.*?>') 
    cleantext = re.sub(CLEANR, ',', raw_html)
    return cleantext


def rota_json(local, rota):
    with open(local.replace(' ', '_') + "_routes.json", 'w') as f:
        f.write(json.dumps(rota, indent=4, ensure_ascii=False))


def string_final_distancia(distancia, string):
    if string.find('Vire') != -1:
        return 'Em ' + distancia + ' ' + string
    else:
        return string + ' por ' + distancia 

def string_distancia(distancia):

    if (distancia.find('km') != -1):
        distancia = distancia.replace(',', '.')
        convert_distancia = re.findall("\d+\.\d+", distancia)
        convert_distancia = float(*convert_distancia)
        
        distancia_final = str(str(convert_distancia) + ' quilometros' if convert_distancia >= 1 else ' quilometro') if convert_distancia >= 1 else (str(int(convert_distancia * 1000)) + ' metros')
        # print(string_final_distancia(distancia_final))
        return distancia_final

    distancia_metros = re.findall("\d+", distancia)
    # print(distancia_metros)
    return str(int(*distancia_metros)) + ' metros'


def instrucao_texto(rota):
    trajetos = []
    
    print('====================== PASSO A PASSO ===========================')
    for index,instrucao in enumerate(rota[0]['legs'][0]['steps'], start=1):
        
        distancia_final = string_distancia(instrucao['distance']['text'])
        caminho = clean(cleanhtml(instrucao['html_instructions']).lower())
        instrucao_final = string_final_distancia(distancia_final, caminho)
        print(str(index) + ')', instrucao_final)
        trajetos.append(instrucao_final)
    print('=================================================================')
    trajetos.append('Você chegou no seu destino!')

    return trajetos
