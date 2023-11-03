from dash import Dash, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.io as pio
from plotly import express as px
import plotly.graph_objs as go

import layout
import utils.data as data
import utils.data_graph as data_graph

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
    df = data.convinar_dataframes(age)
    df_group = data.incidencia_delictiva(df)
    mask = df_group['anio'].isin(age)
    df_group = df_group[mask]
    df_group = data.rellenar_meses_faltantes(df_group, age)
    df_group = data.remplazar_meses(df_group)
    
    # import pdb; pdb.set_trace()
    fig = px.line(df_group, x="mes", y="count", color='anio',text='count', markers=True)
    fig.update_layout(
        title_text='INCIDENCIA DELICTIVA '+str(age),
    )
    fig.update_traces(textposition="bottom right")
    return fig

@callback(
    Output('graph_tab1-1', 'figure'),
    Input('age_tab1-1', 'value'),
    Input('delito_tab1-1', 'value')
)
def graph_delito(age, delito):
    df = data.convinar_dataframes(age)
    df_group = data.incidencia_delictiva(df, ['mes', 'anio', 'id_Grupo'])
    mask = (df_group['anio'].isin(age) & df_group['id_Grupo'].isin([delito]))
    df_group = df_group[mask]
    df_group = data.rellenar_meses_faltantes(df_group, age)
    df_group = data.remplazar_meses(df_group)
    
    fig = px.line(df_group, x="mes", y="count", color='anio', text='count', markers=True)
    fig.update_layout(
        title_text=delito+' '+str(age),
    )
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
    df = data.convinar_dataframes(age)
    df_group = data.incidencia_delictiva(df, ['descripcion', 'id_Grupo', 'anio', 'mes'])
    mask = (df_group['anio'].isin(age) & df_group['descripcion'].isin([distrito]) & df_group['id_Grupo'].isin([delito]))
    df_group = df_group[mask]
    df_group = data.rellenar_meses_faltantes(df_group, age)
    df_group = data.remplazar_meses(df_group)
    
    fig = px.line(df_group, x="mes", y="count", color='anio', text='count', markers=True)
    fig.update_layout(
        title_text=delito+' EN '+distrito+' '+str(age),
    )
    fig.update_traces(textposition="bottom right")
    return fig

@callback(
    Output('graph_tab2-2', 'figure'),
    Input('age_tab2-2', 'value'),
    Input('delito_tab2-2', 'value'),
    Input('Mes_tab2-2', 'value')
)
def graph_mes(anio, delito, mes):
    meses = {
        1: 'ENERO', 2: 'FEBRERO', 3: 'MARZO', 4: 'ABRIL', 5: 'MAYO', 6: 'JUNIO', 
        7: 'JULIO', 8: 'AGOSTO', 9: 'SEPTIEMBRE', 10: 'OCTUBRE', 
        11: 'NOVIEMBRE', 12: 'DICIEMBRE'
    }
    
    df = data.convinar_dataframes(anio)
    mask = (df['anio'].isin(anio)) & (df['id_Grupo'].isin([delito])) & (df['mes'].isin([mes]))
    grupo_df = df[mask]
    grupo_df = data.agregar_divisiones(grupo_df, anio)
    
    fig = px.line(grupo_df, x='descripcion', y='counts', color='anio', text='counts', markers=True)
    fig.update_layout(
        title_text=delito+' EN '+meses[mes]+' '+str(anio),
    )
    fig.update_traces(textposition="bottom right")
    return fig
# Tab 3
@callback(
    Output('graph_tab3', 'figure'),
    Input('age_tab3', 'value'),
    Input('sectores_tab3', 'value'),
)
def graph_map(age, sectores):    
    distritos_df = data_graph.get_distritos()
    
    fig = px.choropleth_mapbox(distritos_df,
                            geojson=distritos_df.geometry,
                            locations=sectores,
                            color=sectores,
                            mapbox_style="open-street-map",
                            zoom=9.3,
                            center={"lat": 31.6, "lon": -106.48333},    
                            opacity=0.3,
                            )
    
    for sector in sectores:
        data_graph.get_sectores(fig, sector)
        data_graph.get_calles(fig, sector)
    
    fig.update_layout(
        autosize=True,
        hovermode='closest',
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True)