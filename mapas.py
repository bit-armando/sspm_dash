import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
from dash import Dash
import geopandas as gpd
import plotly.express as px

# Lee el archivo GeoJSON
geo_df = gpd.read_file('./distritos.geojson')
geo_df = geo_df.set_index('TEXT')

# Configura la aplicación Dash
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=px.choropleth(geo_df, 
                                    geojson=geo_df.geometry.__geo_interface__, 
                                    locations=geo_df.index, 
                                    color='AREA')),
])

if __name__ == '__main__':
    app.run_server(debug=True)