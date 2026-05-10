import plotly.graph_objects as go

def generar_choropleth_colombia(df, geojson, columna_id, columna_valor):
    # Ejemplo tomado de https://community.plotly.com/t/problems-for-insert-a-map-of-colombia-country-in-a-dashboard-with-mapbox/33141
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson,
        locations=df[columna_id],
        z=df[columna_valor],
        colorscale = [
            'rgb(193, 193, 193)',
            'rgb(239,239,239)',
            'rgb(195, 196, 222)',
            'rgb(144,148,194)',
            'rgb(101,104,168)',
            'rgb(65, 53, 132)'
        ],
        colorbar_title="Muertes 2019"
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=4.5,
        mapbox_center={"lat": 4.5708, "lon": -74.2973},
        margin={"r":0,"t":40,"l":0,"b":0},
        title="Mortalidad en Colombia por Departamento"
    )
    
    return fig