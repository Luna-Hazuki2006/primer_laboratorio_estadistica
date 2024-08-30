import csv
import math
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from pprint import pprint

sns.set_theme(style="ticks")

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

def procedimiento(busqueda): 
    r = list(map(lambda x: x[busqueda], cervezas))
    minimo = min(r)
    maximo = max(r)
    n = len(r)
    print(f'Cantidad: {n}')
    oficial = []
    if n >= 25 and n <= 400:
    # if True:  
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
        # pprint(lista)
        real = []
        para = 0
        if amplitud < 1: 
            while True: 
                if minimo > maximo: break
                para = minimo + amplitud 
                clase = {
                    'minimo': minimo, 
                    'maximo': para
                }
                minimo = para + 0.01
                real.append(clase)
        else: 
            while True: 
                if minimo > maximo: break
                para = minimo + amplitud - 1
                clase = {
                    'minimo': minimo, 
                    'maximo': para
                }
                minimo = para + 1
                real.append(clase)
        oficial = [{'clase': real}]
        # pprint(oficial)
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
    plana = list(map(lambda x: x['minimo'], real))
    plana.append(real[-1]['maximo']) 
    diagramar(busqueda, plana)

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
                texto += f' {minimo}-{maximo} |'
            else: texto += f' {todo[esto][i]} |'
        print(len(texto) * '-')
        print(texto)
    print(len(texto) * '-')

def diagramar(busqueda, lista): 
    print(cervezas_pandas)

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
        kde= True
    )
    ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.set_xticks(lista)
    plt.show()

def main(): 
    precios()
    calorias()
    alcohol()

if __name__ == '__main__': 
    main()