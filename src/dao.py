import pandas as pd
import json
from urllib.request import urlopen


class DataLoad:
    # Aquí dataframear
    def __init__(self):
        self.df_no_fetal = pd.read_excel('data/Anexo1.NoFetal2019_CE_15-03-23.xlsx', sheet_name='No_Fetales_2019')
        self.df_codigos_muerte = pd.read_excel('data/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx', header=8, sheet_name='Final')
        self.df_divipola = pd.read_excel('data/Divipola_CE_.xlsx', sheet_name='Hoja1')

        # Formateando
        self.df_codigos_muerte = self.df_codigos_muerte.rename(columns={
            'Código de la CIE-10 cuatro caracteres': 'CODIGOS_MUERTE',
            'Descripcion  de códigos mortalidad a cuatro caracteres': 'DESCRIPCION_MUERTE'
        })

        # Para el de mapa se trae info de un gist publico del mapa de colombia...
        self.url_geojson = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
        with urlopen(self.url_geojson) as response:
            self.counties_json = json.load(response)

        for feature in self.counties_json['features']:
            feature['id'] = feature['properties']['NOMBRE_DPT']