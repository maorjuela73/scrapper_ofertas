from os import listdir
from os.path import isfile, join
import pandas as pd 
import json
from pandas.io.json import json_normalize

mypath= 'vacantes'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

#lista para almacenar los temp_df
frames=[]

#Abre cada archivo json y lo guarda como un temp df
for camino in onlyfiles:
    with open('vacantes/'+camino) as f:
        data = json.load(f)
        temp_df = json_normalize(data)
        frames.append(temp_df)

#concatena todos los temp_df en un solo df        
df=pd.concat(frames)

#Guarda el df como un archivo csv con codificación UTF-8
df.to_csv(r'rd_computrabajo.csv', index = False,encoding='UTF-8')