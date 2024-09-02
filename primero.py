import csv
import math
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from pprint import pprint

sns.set_theme(style='whitegrid')

cervezas_pandas = []
cervezas = []

with open('BEER_proyecto.csv', newline='') as csvfile:
    partes = csv.DictReader(csvfile, delimiter=';')
    for esto in partes: 
        esto['PrecioDolares'] = float(esto['PrecioDolares'])
        esto['Calorias'] = float(esto['Calorias'])
        if float(esto['PorcAlcohol']) == 0.0: 
            esto['PorcAlcohol'] = 0.01
        else: 
            esto['PorcAlcohol'] = float(esto['PorcAlcohol'])
        if esto['PaisOrigen'] == '0': esto['PaisOrigen'] = 'EU'
        elif esto['PaisOrigen'] == '1': esto['PaisOrigen'] = 'Importada'
        if esto['TipoCerveza'] == '1': esto['TipoCerveza'] = 'lager artesanal'
        elif esto['TipoCerveza'] == '2': esto['TipoCerveza'] = 'clara artesanal'
        elif esto['TipoCerveza'] == '3': esto['TipoCerveza'] = 'lager importada'
        elif esto['TipoCerveza'] == '4': esto['TipoCerveza'] = 'cerveza normal y helada'
        elif esto['TipoCerveza'] == '5': esto['TipoCerveza'] = 'cerveza baja en caloríasy sin alcohol'
        cervezas.append(esto)
    cervezas_pandas = pd.DataFrame(cervezas)

def precios(): 
    procedimiento('PrecioDolares')

def calorias(): 
    procedimiento('Calorias')

# Por la forma de datos usar datos no agrupados
# El 0 para python lo considera inexistente por eso se le tuvo que hacer una
# Pequeña modificación muy cerca del 0 
def alcohol(): 
    procedimiento('PorcAlcohol')

def tipos(): 
    lista = ['lager artesanal', 'clara artesanal', 'lager importada', 
             'cerveza normal y helada', 'cerveza baja en caloríasy sin alcohol']
    print(lista)
    diagramar('TipoCerveza', lista)

def paises(): 
    lista = ['EU', 'Importada']
    print(lista)
    diagramar('PaisOrigen', lista)

def procedimiento(busqueda): 
    r = list(map(lambda x: x[busqueda], cervezas))
    minimo = min(r)
    maximo = max(r)
    n = len(r)
    print(f'Cantidad: {n}')
    oficial = []
    if n >= 25 and n <= 400:
        rango = maximo - minimo 
        k = 1 + 3.3 * math.log(n, 10)
        amplitud = rango / k
        print(f'Amplitud: {amplitud}')
        if amplitud > float(amplitud): 
            amplitud += 1
            amplitud = float(amplitud)
        lista = {}
        for esto in r: 
            try: lista[esto] += 1
            except: lista[esto] = 1
        real = []
        para = 0
        while True: 
            if minimo > maximo: break
            if amplitud < 1: para = minimo + amplitud 
            else: para = minimo + amplitud - 1
            clase = {
                'minimo': round(minimo, 2), 
                'maximo': round(para, 2)
            }
            if amplitud < 1: minimo = para + 0.01
            else: minimo = para + 1
            real.append(clase)
        oficial = [{'clase': real}]
        oficial[0]['fi'] = []
        for esto in real: 
            numero = 0
            llaves = list(filter(lambda x: x >= esto['minimo'] and x <= esto['maximo'], lista.keys()))
            for una in llaves: 
                numero += lista[una]
            # for i in range(int(esto['minimo']), int(esto['maximo']) + 1): 
            #     try: numero += lista[i]
            #     except: continue
            oficial[0]['fi'].append(numero)
        parte = []
        for esto in oficial[0]['fi']: 
            if len(parte) >= 1: parte.append(esto + parte[-1])
            else: parte.append(esto)
        oficial[0]['fa'] = parte
        oficial[0]['xi'] = list(map(lambda x: (x['minimo'] + x['maximo']) / 2, oficial[0]['clase']))
    else: 
        todos = list(map(lambda x: float(x), r))
        lista = {}
        for esto in todos: 
            try: lista[esto] += 1
            except: lista[esto] = 1
        pprint(lista)
        print(len(lista.items()))
        return
    oficial[0]['fi.xi'] = [(xi * fi) for xi, fi in zip(oficial[0]['fi'], oficial[0]['xi'])]
    oficial[0]['fsr'] = list(map(lambda x: x / oficial[0]['fa'][-1], oficial[0]['fi']))
    oficial[0]['far'] = list(map(lambda x: x / oficial[0]['fa'][-1], oficial[0]['fa']))
    oficial[0]['fsr%'] = list(map(lambda x: x * 100, oficial[0]['fsr']))
    oficial[0]['far%'] = list(map(lambda x: x * 100, oficial[0]['far']))
    oficial[0]['fi.xi^2'] = [(xi * fixi) for xi, fixi in zip(oficial[0]['fi.xi'], oficial[0]['xi'])]
    mostrar_tabla(oficial)
    print('*' * 50)
    total = oficial[0]['fa'][-1]
    # print(f'Amplitud: {amplitud}')
    print('Datos de posición: ')
    cuartiles = []
    for i in range(1, 5): 
        q = obtencion(oficial[0], ((25 * i) / 100) * total)
        print(f'{i}° cuartil: {round(q, 4)}')
        cuartiles.append(q)
    print('Datos de centralización: ')
    media = sum(oficial[0]['fi.xi']) / total
    print(f'Media aritmética: {round(media, 4)}')
    calculo = total / 2
    fa = 0
    for esto in oficial[0]['fa']: 
        if esto >= calculo: 
            fa = esto
            break
    indice = oficial[0]['fa'].index(fa)
    li = oficial[0]['clase'][indice]['minimo']
    fi_menos = oficial[0]['fa'][indice - 1]
    fi = oficial[0]['fi'][indice]
    mediana = li + ((calculo - fi_menos) / fi) * amplitud
    print(f'Mediana: {round(mediana, 4)}')
    lugares_modales = buscar_modales(oficial[0]['fi'])
    modales = []
    for esto in lugares_modales: 
        li = oficial[0]['clase'][esto]['minimo']
        fi = oficial[0]['fi'][esto]
        try: fi_menos = oficial[0]['fi'][esto - 1]
        except: fi_menos = 0
        try: fi_mas = oficial[0]['fi'][esto + 1]
        except: fi_mas = 0
        d1 = fi - fi_menos
        d2 = fi - fi_mas
        modal = li + (d1 / (d1 + d2)) * amplitud
        modales.append(modal)
    print(f'Modales: {[round(esto, 4) for esto in modales]}')
    print('Datos de variabilidad: ')
    varianza = (sum(oficial[0]['fi.xi^2']) / total) - (media ** 2)
    print(f'Varianza: {round(varianza, 4)}')
    desviacion = math.sqrt(varianza)
    print(f'Desviación típica: {round(desviacion, 4)}')
    coeficiente = (desviacion / media) * 100
    print(f'Coeficiente de variación: {round(coeficiente, 4)}%')
    intercuartil = cuartiles[2] - cuartiles[0]
    print(f'Rango intercuartil: {round(intercuartil, 4)}')
    print('Datos de forma: ')
    p75 = obtencion(oficial[0], (75 / 100) * total)
    p25 = obtencion(oficial[0], (25 / 100) * total)
    p90 = obtencion(oficial[0], (90 / 100) * total)
    p10 = obtencion(oficial[0], (10 / 100) * total)
    curtosis = ((p75 - p25) / (p90 - p10)) * 0.5
    if curtosis == 0: apuntamiento = 'Es mesocúrtica como la normal'
    elif curtosis > 0: apuntamiento = 'Es leptocúrtica apuntada'
    elif curtosis < 0: apuntamiento = 'Es platicúrtica aplanada'
    print(f'Curtosis: {round(curtosis, 4)} ({apuntamiento})')
    indice = (3 * (media - mediana)) / desviacion
    if indice == 0: simetria = 'Es simétrica'
    elif indice > 0: simetria = 'Es asimétrica positiva con sesgo a la derecha'
    elif indice < 0: simetria = 'Es asimétrica negativa con sesgo a la izquierda'
    print(f'Índice de asimetría: {round(indice, 4)} ({simetria})')
    if busqueda == 'PorcAlcohol': 
        primera = (5.5 - media) / desviacion
        resultado = 0.7794 * 100
        print(f'La probabilidad de que el alcohol sea menor a 5.5 es: {resultado}%')
    plana = list(map(lambda x: x['minimo'], real))
    plana.append(real[-1]['maximo']) 
    if busqueda == 'PrecioDolares': 
        segunda = (4.5 - media) / desviacion
        resultado = (1 - 0.3557) * 100
        print(f'Pocentaje mayor 4.5 de precios es: {resultado}%')
    if busqueda == 'Calorias': 
        primera = (150 - media) / desviacion
        segunda = (180 - media) / desviacion
        res1 = 1 - 0.5948 
        res2 = 0.5793
        resultado = (res2 - res1) * 100
        print(f'Porcentaje de que las calorías estén entre 150 y 180: {resultado}%')
    print('*' * 50)
    diagramar(busqueda, plana)

def buscar_modales(fi : list): 
    lista = []
    maximo = max(fi)
    for i in range(len(fi)): 
        if fi[i] == maximo: 
            lista.append(i)
    return lista

def mostrar_tabla(todo : dict): 
    todo = todo[0]
    total = len(todo['clase'])
    llaves = todo.keys()
    texto = '|'
    for esto in llaves: texto += f' {esto} |'
    print(len(texto) * '-')
    print(texto)
    for i in range(total): 
        texto = '|'
        for esto in llaves: 
            if esto == 'clase': 
                minimo = todo[esto][i]['minimo']
                maximo = todo[esto][i]['maximo']
                texto += f' {round(minimo, 4)}-{round(maximo, 4)} |'
            else: texto += f' {round(todo[esto][i], 4)} |'
        print(len(texto) * '-')
        print(texto)
    print(len(texto) * '-')

def obtencion(lista, numero): 
    fa = lista['fa']
    fi = lista['fi']
    clase = lista['clase']
    indice = 0
    for esto in fa: 
        if esto >= numero: 
            indice = fa.index(esto)
            break
    fa_numero = fa[indice - 1]
    fi_numero = fi[indice]
    li = clase[indice]['minimo']
    amplitud = clase[0]['maximo'] - clase[0]['minimo']
    esto = li + ((numero - fa_numero) / fi_numero) * amplitud
    return esto

def diagramar(busqueda, lista): 
    # pprint(cervezas_pandas)

    f, ax = plt.subplots(figsize=(7, 5))
    sns.despine(f)

    sns.histplot(
        cervezas_pandas,
        x=busqueda, 
        # hue="TipoCerveza",
        # multiple="stack",
        # palette="light:m_r",
        edgecolor=".3",
        linewidth=.5,
        log_scale=True, 
        # discrete= True, 
        kde=(True if busqueda != 'PaisOrigen' and busqueda != 'TipoCerveza' else False) 
    )
    ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.set_xticks(lista)
    plt.show()

def main(): 
    tipos()
    paises()
    precios()
    calorias()
    alcohol()

if __name__ == '__main__': 
    main()