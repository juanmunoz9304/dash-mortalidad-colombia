import plotly.express as px


def generar_line_plot(df): 
    fig = px.line(df, x="MES_NOMBRE", y="TOTAL", labels={'MES_NOMBRE': 'Mes'}, title='Muertes por mes en Colombia 2019')
    return fig