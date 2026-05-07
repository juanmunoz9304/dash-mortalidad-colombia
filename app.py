import pandas as pd
import dash
from dash import dcc, html, Input, Output, ctx
import json
import unicodedata
from urllib.request import urlopen
from plots.maps import generar_choropleth_colombia

# Formatear
def normalizar_texto(texto):
    if not isinstance(texto, str): return ""
    return ''.join(c for c in unicodedata.normalize('NFD', texto) 
                  if unicodedata.category(c) != 'Mn').upper().strip()

def preparar_datos_mortalidad():
    df_m = pd.read_excel('data/Anexo1.NoFetal2019_CE_15-03-23.xlsx', sheet_name='No_Fetales_2019')
    df_d = pd.read_excel('data/Divipola_CE_.xlsx', sheet_name='Hoja1')
    resumen = df_m.groupby('COD_DEPARTAMENTO').size().reset_index(name='TOTAL')
    nombres = df_d[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates()
    df_final = pd.merge(resumen, nombres, on='COD_DEPARTAMENTO')
    df_final['ID_MAPA'] = df_final['DEPARTAMENTO'].apply(normalizar_texto)
    mapeo = {'BOGOTA, D.C.': 'BOGOTA D.C.', 'NORTE DE SANTANDER': 'NORTE SANTANDER'}
    df_final['ID_MAPA'] = df_final['ID_MAPA'].replace(mapeo)
    return df_final

# Para el de mapa se trae info de un gits publico del mapa de colombia...
app = dash.Dash(__name__)
server = app.server

url_geojson = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
with urlopen(url_geojson) as response:
    counties_json = json.load(response)

for feature in counties_json['features']:
    feature['id'] = feature['properties']['NOMBRE_DPT']

df_listo = preparar_datos_mortalidad()

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
        fig_mapa = generar_choropleth_colombia(
            df=df_listo, 
            geojson=counties_json, 
            columna_id='ID_MAPA', 
            columna_valor='TOTAL'
        )
        return dcc.Graph(id='mapa-principal', figure=fig_mapa, style={'height': '100%'})

    elif button_id == 'btn-lineas':
        return html.Div([html.H3("Gráfico de Líneas (En desarrollo)")])

    elif button_id == 'btn-barras':
        return html.Div([html.H3("Gráfico de Barras (En desarrollo)")])
        
    elif button_id == 'btn-circular':
        return html.Div([html.H3("Gráfico Circular (En desarrollo)")])
        
    elif button_id == 'btn-tabla':
        return html.Div([html.H3("Tabla de Datos (En desarrollo)")])
        
    elif button_id == 'btn-barras-apiladas':
        return html.Div([html.H3("Barras Apiladas (En desarrollo)")])
        
    elif button_id == 'btn-histograma':
        return html.Div([html.H3("Histograma (En desarrollo)")])

    return html.Div("Seleccione un gráfico")

if __name__ == "__main__":
    app.run(debug=True)