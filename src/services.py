import unicodedata
import pandas as pd

class Services:

    def __init__(self, df):
        self.repo = df

    
    def normalizar_texto(self, texto):
        if not isinstance(texto, str): return ""
        return ''.join(c for c in unicodedata.normalize('NFD', texto) 
                    if unicodedata.category(c) != 'Mn').upper().strip()

    # Mapa
    def preparar_datos_mortalidad(self):
        resumen = self.repo.df_no_fetal.groupby('COD_DEPARTAMENTO').size().reset_index(name='TOTAL')
        nombres = self.repo.df_divipola[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates()
        df_final = pd.merge(resumen, nombres, on='COD_DEPARTAMENTO')
        df_final['ID_MAPA'] = df_final['DEPARTAMENTO'].apply(self.normalizar_texto)
        mapeo = {'BOGOTA, D.C.': 'BOGOTA D.C.', 'NORTE DE SANTANDER': 'NORTE SANTANDER'}
        df_final['ID_MAPA'] = df_final['ID_MAPA'].replace(mapeo)
        return df_final

    # Lineas
    def preparar_mortalidad_mes(self):
        df_mes = self.repo.df_no_fetal.groupby('MES').size().reset_index(name='TOTAL')
        meses_nombres = {
            1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio',
            7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'novimebre', 12: 'diciembre'
        }
        df_mes['MES_NOMBRE'] = df_mes['MES'].map(meses_nombres)
        return df_mes

    # Barras
    def preparar_ciudades_mas_violentas(self):
        # Códigos de X95 y sus traducciones según el excel
        codigos_violencia = ['X950', 'X951', 'X952', 'X953', 'X954', 'X955', 'X956', 'X957', 'X958', 'X959']

        # Filtrar y ordenar
        df_violentos = self.repo.df_no_fetal[self.repo.df_no_fetal['COD_MUERTE'].isin(codigos_violencia)].copy()
        homicidios_group = df_violentos.groupby('COD_DANE').size().reset_index(name='HOMICIDIOS').sort_values(by='HOMICIDIOS', ascending=False)

        # relacionar
        homicidios_group['COD_DANE'] = homicidios_group['COD_DANE'].astype(int)
        self.repo.df_divipola['COD_DANE'] = self.repo.df_divipola['COD_DANE'].astype(int)

        # cruzar datos
        df_relacionado = pd.merge(
            homicidios_group, 
            self.repo.df_divipola[['COD_DANE', 'MUNICIPIO']], 
            on='COD_DANE'
        ).head(5)
        return df_relacionado

    # Pie
    def preparar_ciudades_menor_mortalidad(self):
        conteo_group = self.repo.df_no_fetal.groupby('COD_DANE').size().reset_index(name='TOTAL').sort_values(by='TOTAL', ascending=True)

        conteo_group['COD_DANE'] = conteo_group['COD_DANE'].astype(int)
        self.repo.df_divipola['COD_DANE'] = self.repo.df_divipola['COD_DANE'].astype(int)

        df_relacionado = pd.merge(
            conteo_group, 
            self.repo.df_divipola[['COD_DANE', 'MUNICIPIO']], 
            on='COD_DANE'
        ).head(10)
        
        return df_relacionado