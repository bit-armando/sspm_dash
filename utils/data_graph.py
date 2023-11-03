import pandas as pd
import geopandas as gpd
import plotly.graph_objs as go

def get_distritos():
    df = gpd.read_file('./distritos.geojson')
    df = df.set_index('TEXT')
    return df

def get_sectores(fig, distrito):
    # Lee el archivo geojson y lo filtra por distrito
    geo_df = gpd.read_file('./sectores.geojson')
    mask = geo_df['Distrito'].isin([distrito])
    geo_df = geo_df[mask]

    # Agrega los sectores al mapa
    boundaries = geo_df['geometry'].boundary.values
    coords = [list(boundary.coords) for boundary in boundaries]
    
    for line in coords:
        fig.add_trace(go.Scattermapbox(
                lat=[coord[1] for coord in line],
                lon=[coord[0] for coord in line],
                mode='lines',
                line=dict(width=1, color='black'),
                showlegend=False,
                ))
    
    # Agrega el numero del sector al mapa
    for centroide, distrito in zip(geo_df['geometry'].centroid, geo_df['Sector'].values):        
        fig.add_trace(go.Scattermapbox(
                lat=[centroide.y],
                lon=[centroide.x],
                mode='text',
                marker=go.scattermapbox.Marker(
                    size=5,
                    opacity=0.5
                ),
                text=[distrito],
                showlegend=False
            ))

def get_calles(fig, distrito):
    df = pd.read_csv('./data_group/locations.csv', index_col=0)
    mask = df['distrito'].isin([distrito])
    df = df[mask]

    fig.add_trace(
        go.Scattermapbox(
            lat=df['lat'],
            lon=df['lon'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=5,
                opacity=0.5,
                color='red'
            ),
            showlegend=False
        )
    )