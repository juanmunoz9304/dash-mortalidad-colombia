import plotly.express as px


def generar_pie_plot(df): 
    fig = px.pie(df, values='TOTAL', names='MUNICIPIO', title='10 Ciudades con Menor Mortalidad')
    return fig