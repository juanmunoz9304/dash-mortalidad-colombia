import plotly.express as px


def generar_bar_plot(df): 
    fig = px.bar(df, x='MUNICIPIO', y='HOMICIDIOS', title='Ciudades con Mayor Número de Homicidios (Arma de Fuego - 2019)',
                 labels={'MUNICIPIO': 'Ciudad', 'HOMICIDIOS': 'Cantidad de Casos'})
    return fig



def generar_multi_bar_plot(df): 
    fig = px.bar(df, x='DEPARTAMENTO', y='TOTAL', color='SEXO', barmode='stack', title='Mortalidad por genero en departamentos',
                 labels={'DEPARTAMENTO': 'Departamento', 'TOTAL': 'Cantidad de Casos'})
    return fig