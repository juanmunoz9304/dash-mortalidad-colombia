import plotly.graph_objects as go

def generar_choropleth_colombia(df, geojson, columna_id, columna_valor):
    """
    Recibe la data ya formateada y el GeoJSON para pintar el mapa.
    """
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson,
        locations=df[columna_id],
        z=df[columna_valor],
        colorscale='Reds',
        marker_opacity=0.7,
        marker_line_width=0.5,
        colorbar_title="Muertes 2019"
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=4.2,
        mapbox_center={"lat": 4.5708, "lon": -74.2973},
        margin={"r":0,"t":40,"l":0,"b":0},
        title="Mortalidad en Colombia por Departamento"
    )
    
    return fig