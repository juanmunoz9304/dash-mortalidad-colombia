import pandas as pd
import dash
from dash import dcc, html, Input, Output, ctx
from plots import maps, line, bar, pie
from src import dao, services

# Formatear

df = dao.DataLoad()
sv = services.Services(df)

app = dash.Dash(__name__)
server = app.server

df_mapa_completo = sv.preparar_datos_mortalidad()
df_linea_completo = sv.preparar_mortalidad_mes()
df_barra_completo = sv.preparar_ciudades_mas_violentas()
df_circular_completo = sv.preparar_ciudades_menor_mortalidad()

# layout general
app.layout = html.Div([
    html.H1("Análisis de Mortalidad Colombia 2019", style={'textAlign': 'center'}),
    
    html.Div(id='contenedor-graficos', style={'height': '75vh'}),
    
    # Botones siempre disponibles en la parte inferior con el div
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
            geojson=df.counties_json, 
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