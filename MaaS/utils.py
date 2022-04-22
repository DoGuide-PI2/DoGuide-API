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
    string = string.replace('II ', '2')
    string = string.replace('Road', 'Avenida')
    string = string.replace('road', 'Avenida')
    string = string.replace('Estrada de uso restrito', '')
    string = string.replace('estrada de uso restrito', '')
    string = string.replace('&nbsp', '')

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
    for instrucao in rota[0]['legs'][0]['steps']:
        
        distancia_final = string_distancia(instrucao['distance']['text'])
        caminho = clean(cleanhtml(instrucao['html_instructions']))
        instrucao_final = string_final_distancia(distancia_final, caminho)
        print(instrucao_final)
        trajetos.append(instrucao_final)
    trajetos.append('Você chegou no seu destino!')

    return trajetos




def gerador_poligno_retangulo(pontoInicial, pontoFinal, size = 0.00005):
    pontoSuperior1 = (pontoInicial[0], pontoInicial[1] + size)
    pontoInferior1 = (pontoInicial[0], pontoInicial[1] - size)
        
    pontoSuperior2 = (pontoFinal[0], pontoFinal[1] + size)
    pontoInferior2 = (pontoFinal[0], pontoFinal[1] - size)
    
    lista = []
    lista.append(pontoSuperior1)
    lista.append(pontoSuperior2)
    lista.append(pontoInferior2)
    lista.append(pontoInferior1)

    return [pontoSuperior1, pontoSuperior2, pontoInferior2, pontoInferior1]


def area(x1, y1, x2, y2, x3, y3):	
	return abs((x1 * (y2 - y3) +
				x2 * (y3 - y1) +
				x3 * (y1 - y2)) / 2.0)


def checagem_percurso_poligonal(x1, y1, x2, y2, x3, y3, x4, y4, x, y):
    A = (area(x1, y1, x2, y2, x3, y3) + area(x1, y1, x4, y4, x3, y3))
    A1 = area(x, y, x1, y1, x2, y2)
    A2 = area(x, y, x2, y2, x3, y3)
    A3 = area(x, y, x3, y3, x4, y4)
    A4 = area(x, y, x1, y1, x4, y4)
    B = A1 + A2 + A3 + A4
    print(A, B)
    return abs(A - B) <= max(1e-09 * max(abs(A), abs(B)), 0.0)

