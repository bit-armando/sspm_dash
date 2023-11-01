import plotly.graph_objects as go
import geopandas as gpd

# Suponiendo que 'a' es un GeoDataFrame de GeoPandas
a = gpd.read_file('./sectores.geojson')
boundaries = a['geometry'].boundary

# Crear una figura vacía
fig = go.Figure()

# Añadir una traza para cada límite
for boundary in boundaries:
    # Extraer las coordenadas x e y
    x, y = boundary.xy
    # Añadir la traza
    fig = go.Scatter(x=x, y=y, mode='lines')

fig.show()