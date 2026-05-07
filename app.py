import pandas as pd
import dash
from dash import dcc, html, Input, Output, ctx
import json
import unicodedata
from urllib.request import urlopen
from plots import maps, line, bar, pie

# Formatear

# Aquí dataframear
df_no_fetal = pd.read_excel('data/Anexo1.NoFetal2019_CE_15-03-23.xlsx', sheet_name='No_Fetales_2019')
df_codigos_muerte = pd.read_excel('data/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx', sheet_name='Final')
df_divipola = pd.read_excel('data/Divipola_CE_.xlsx', sheet_name='Hoja1')

def normalizar_texto(texto):
    if not isinstance(texto, str): return ""
    return ''.join(c for c in unicodedata.normalize('NFD', texto) 
                  if unicodedata.category(c) != 'Mn').upper().strip()

# Mapa
def preparar_datos_mortalidad():
    resumen = df_no_fetal.groupby('COD_DEPARTAMENTO').size().reset_index(name='TOTAL')
    nombres = df_divipola[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates()
    df_final = pd.merge(resumen, nombres, on='COD_DEPARTAMENTO')
    df_final['ID_MAPA'] = df_final['DEPARTAMENTO'].apply(normalizar_texto)
    mapeo = {'BOGOTA, D.C.': 'BOGOTA D.C.', 'NORTE DE SANTANDER': 'NORTE SANTANDER'}
    df_final['ID_MAPA'] = df_final['ID_MAPA'].replace(mapeo)
    return df_final

# Lineas
def preparar_mortalidad_mes():
    df_mes = df_no_fetal.groupby('MES').size().reset_index(name='TOTAL')
    meses_nombres = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio',
        7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'novimebre', 12: 'diciembre'
    }
    df_mes['MES_NOMBRE'] = df_mes['MES'].map(meses_nombres)
    return df_mes

# Barras
def preparar_ciudades_mas_violentas():
    # Códigos de X95 y sus traducciones según el excel
    codigos_violencia = ['X950', 'X951', 'X952', 'X953', 'X954', 'X955', 'X956', 'X957', 'X958', 'X959']

    # Filtrar y ordenar
    df_violentos = df_no_fetal[df_no_fetal['COD_MUERTE'].isin(codigos_violencia)].copy()
    homicidios_group = df_violentos.groupby('COD_DANE').size().reset_index(name='HOMICIDIOS').sort_values(by='HOMICIDIOS', ascending=False)

    # relacionar
    homicidios_group['COD_DANE'] = homicidios_group['COD_DANE'].astype(int)
    df_divipola['COD_DANE'] = df_divipola['COD_DANE'].astype(int)

    # cruzar datos
    df_relacionado = pd.merge(
        homicidios_group, 
        df_divipola[['COD_DANE', 'MUNICIPIO']], 
        on='COD_DANE'
    ).head(5)
    return df_relacionado

# Pie
def preparar_ciudades_menor_mortalidad():
    conteo_group = df_no_fetal.groupby('COD_DANE').size().reset_index(name='TOTAL').sort_values(by='TOTAL', ascending=True)

    conteo_group['COD_DANE'] = conteo_group['COD_DANE'].astype(int)
    df_divipola['COD_DANE'] = df_divipola['COD_DANE'].astype(int)

    df_relacionado = pd.merge(
        conteo_group, 
        df_divipola[['COD_DANE', 'MUNICIPIO']], 
        on='COD_DANE'
    ).head(10)
    
    return df_relacionado

# Para el de mapa se trae info de un gits publico del mapa de colombia...
app = dash.Dash(__name__)
server = app.server

url_geojson = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
with urlopen(url_geojson) as response:
    counties_json = json.load(response)

for feature in counties_json['features']:
    feature['id'] = feature['properties']['NOMBRE_DPT']

df_mapa_completo = preparar_datos_mortalidad()
df_linea_completo = preparar_mortalidad_mes()
df_barra_completo = preparar_ciudades_mas_violentas()
df_circular_completo = preparar_ciudades_menor_mortalidad()

# layout general
app.layout = html.Div([
    html.H1("Análisis de Mortalidad Colombia 2019", style={'textAlign': 'center'}),
    
    html.Div(id='contenedor-graficos', style={'height': '75vh'}),
    
    # Botones siempre disponibles en la parte inferior
    html.Div([
        html.Button('Ver grafico Mapa', id='btn-mapa', n_clicks=0),
        html.Button('Ver grafico Lineas', id='btn-lineas', n_clicks=0),
        html.Button('Ver grafico Barras', id='btn-barras', n_clicks=0),
        html.Button('Ver grafico Circular', id='btn-circular', n_clicks=0),
        html.Button('Ver Tabla', id='btn-tabla', n_clicks=0),
        html.Button('Ver grafico Barras apiladas', id='btn-barras-apiladas', n_clicks=0),
        html.Button('Ver histograma', id='btn-histograma', n_clicks=0),
    ], style={'textAlign': 'center', 'marginTop': '20px'})
])

@app.callback(
    Output('contenedor-graficos', 'children'),
    [Input('btn-mapa', 'n_clicks'),
     Input('btn-lineas', 'n_clicks'),
     Input('btn-barras', 'n_clicks'),
     Input('btn-circular', 'n_clicks'),
     Input('btn-tabla', 'n_clicks'),
     Input('btn-barras-apiladas', 'n_clicks'),
     Input('btn-histograma', 'n_clicks')]
)
def mostrar_grafico(*args):
    button_id = ctx.triggered_id

    # Lógica de renderizado según el ID del botón
    if button_id == 'btn-mapa' or button_id is None:
        fig_mapa = maps.generar_choropleth_colombia(
            df=df_mapa_completo, 
            geojson=counties_json, 
            columna_id='ID_MAPA', 
            columna_valor='TOTAL'
        )
        return dcc.Graph(id='mapa-principal', figure=fig_mapa, style={'height': '100%'})

    elif button_id == 'btn-lineas':
        fig_line = line.generar_line_plot(df=df_linea_completo)
        return dcc.Graph(id='line-plot', figure=fig_line, style={'height': '100%'})

    elif button_id == 'btn-barras':
        fig_barra = bar.generar_bar_plot(df=df_barra_completo)
        return dcc.Graph(id='bar-plot', figure=fig_barra, style={'height': '100%'})
        
    elif button_id == 'btn-circular':
        fig_circular = pie.generar_pie_plot(df=df_circular_completo)
        return dcc.Graph(id='pie-plot', figure=fig_circular, style={'height': '100%'})
        
    elif button_id == 'btn-tabla':
        return html.Div([html.H3("Tabla de Datos (En desarrollo)")])
        
    elif button_id == 'btn-barras-apiladas':
        return html.Div([html.H3("Barras Apiladas (En desarrollo)")])
        
    elif button_id == 'btn-histograma':
        return html.Div([html.H3("Histograma (En desarrollo)")])

    return html.Div("Seleccione un gráfico")

if __name__ == "__main__":
    app.run(debug=True)