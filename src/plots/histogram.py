import plotly.express as px

def generar_histogram_plot(df): 
    fig = px.histogram(df, x='CATEGORIA_EDAD', y='CONTEO', category_orders=dict(CATEGORIA_EDAD =['Mortalidad neonatal', 'Mortalidad infantil', 
                                                                            'Primera infancia', 'Niñez','Adolescencia', 
                                                                            'Juventud', 'Adultez temprana', 
                                                                            'Adultez intermedia','Vejez', 'Longevidad', 
                                                                            'Edad desconocida']),
                                                                            histfunc='avg')
    
    fig.update_layout(
        bargap=0
    )
    return fig
