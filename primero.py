import csv
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from pprint import pprint

sns.set_theme(style="ticks")

diamonds = sns.load_dataset("diamonds")
# print(diamonds)

with open('BEER_proyecto.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    lista = []
    cabeza = []
    for row in reader: 
        esto = row
        try: 
            esto[1] = float(esto[1])
            esto[2] = float(esto[2])
            esto[3] = float(esto[3])
            cabeza.append(esto)
        except: lista.append(esto)
    diamonds = pd.DataFrame(lista, columns=cabeza)
    # reader = csv.DictReader(csvfile, delimiter=';')
    # for row in reader:
    #     print(row)

print(diamonds)

f, ax = plt.subplots(figsize=(7, 5))
sns.despine(f)

sns.histplot(
    diamonds,
    x="PrecioDolares", 
    # hue="cut",
    # multiple="dodge",
    # palette="light:m_r",
    edgecolor=".3",
    linewidth=.5,
    log_scale=True,
    # discrete= True, 
    kde= True
)
ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
ax.set_xticks([500, 1000, 2000, 5000, 10000])
plt.show()
