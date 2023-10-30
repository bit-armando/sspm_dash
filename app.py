from dash import Dash, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.io as pio
from plotly import express as px

import layout
import utils.data as data
import utils.data_graph as data_graph

df = data.convinar_dataframes('./data/')
df = data.agregar_fecha(df)

TEMPLATE_LIGHT = "plotly_white"
TEMPLATE_DARK = "cyborg"

pio.templates.default = TEMPLATE_LIGHT

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = layout.layout


# Tab 1
@callback(
    Output('graph_tab1', 'figure'),
    Input('age_tab1', 'value')
)
def graph_age(age):
    df_group = data.incidencia_delictiva(df)
    mask = df_group['anio'].isin(age)
    df_group = df_group[mask]
    df_group = data.rellenar_meses_faltantes(df_group, age)
    df_group = data.remplazar_meses(df_group)
    
    # import pdb; pdb.set_trace()
    fig = px.line(df_group, x="mes", y="count", color='anio',text='count', markers=True)
    fig.update_traces(textposition="bottom right")
    return fig

@callback(
    Output('graph_tab1-1', 'figure'),
    Input('age_tab1-1', 'value'),
    Input('delito_tab1-1', 'value')
)
def graph_delito(age, delito):
    df_group = data.incidencia_delictiva(df, ['mes', 'anio', 'id_Grupo'])
    mask = (df_group['anio'].isin(age) & df_group['id_Grupo'].isin([delito]))
    df_group = df_group[mask]
    df_group = data.rellenar_meses_faltantes(df_group, age)
    df_group = data.remplazar_meses(df_group)
    
    fig = px.line(df_group, x="mes", y="count", color='anio', text='count', markers=True)
    fig.update_traces(textposition="bottom right")
    return fig


# Tab 2
@callback(
    Output('graph_tab2', 'figure'),
    Input('age_tab2', 'value'),
    Input('distrito_tab2', 'value'),
    Input('delito_tab2', 'value')
)
def graph_distrito(age, distrito, delito):
    df_group = data.incidencia_delictiva(df, ['descripcion', 'id_Grupo', 'anio', 'mes'])
    mask = (df_group['anio'].isin(age) & df_group['descripcion'].isin([distrito]) & df_group['id_Grupo'].isin([delito]))
    df_group = df_group[mask]
    df_group = data.rellenar_meses_faltantes(df_group, age)
    df_group = data.remplazar_meses(df_group)
    
    fig = px.line(df_group, x="mes", y="count", color='anio', text='count', markers=True)
    fig.update_traces(textposition="bottom right")
    return fig

@callback(
    Output('graph_tab2-2', 'figure'),
    Input('age_tab2-2', 'value'),
    Input('delito_tab2-2', 'value'),
    Input('Mes_tab2-2', 'value')
)
def graph_mes(anio, delito, mes):
    grupo_df = df.groupby(['descripcion', 'id_Grupo', 'anio', 'mes']).size().reset_index(name='counts')
    mask = (grupo_df['anio'].isin(anio)) & (grupo_df['id_Grupo'].isin([delito])) & (grupo_df['mes'].isin([mes]))
    grupo_df = grupo_df[mask]
    # grupo_df = data.agregar_distritos(grupo_df, anio)
    
    fig = px.line(grupo_df, x='descripcion', y='counts', color='anio', text='counts', markers=True)
    fig.update_traces(textposition="bottom right")
    return fig
# Tab 3
@callback(
    Output('graph_tab3', 'figure'),
    Input('age_tab3', 'value'),
)
def graph_map(age):    
    distritos_df = data_graph.data_maps()
    calles_df = data_graph.data_calles()
    fig = px.choropleth_mapbox(distritos_df,
                            geojson=distritos_df.geometry,
                            locations=distritos_df.index,
                            color=distritos_df.index,
                            mapbox_style="open-street-map",
                            zoom=9.3,
                            center={"lat": 31.6, "lon": -106.48333},                            opacity=0.5,
                            )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.add_trace(px.scatter_mapbox(calles_df, lat='lat', lon='lon', hover_name='distrito', size_max=15).data[0])
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


if __name__ == '__main__':
    app.run(debug=True)

# mapas recomendados [open-street-map, carto-positron, stamen-terrain, ]