from dash import Dash, callback, Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.io as pio
from plotly import express as px
from dash import html

import layout
import utils.data as data
import utils.data_graph as data_graph

import pandas as pd
import base64
import io
import sqlite3

TEMPLATE = "seaborn"

pio.templates.default = TEMPLATE

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = layout.layout

# Document
@callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def subir_archivo(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                df = data.limpiar_data_incidentes(df)
                data.get_points_from_incidentes(df)
                locations = pd.read_csv('data_group/locations.csv')
                
        except Exception as e:
            print(e)
            return html.Div(['Hubo un error procesando este archivo.'])
        
        connection = sqlite3.connect('Estadisticas.db')
        locations.to_sql('Incidentes', connection, if_exists='replace', index=False)
        return html.Div(['Archivo subido exitosamente.'])
    else:
        raise PreventUpdate

# Tab 1
@callback(
    Output('graph_tab1', 'figure'),
    Input('age_tab1', 'value')
)
def graph_age(age):
    df = data.get_data_incidentes()
    df_group = data.incidencia_delictiva(df)
    mask = df_group['anio'].isin(age)
    df_group = df_group[mask]
    df_group = data.rellenar_meses_faltantes(df_group, age)
    df_group = data.remplazar_meses(df_group)
    
    fig = px.line(df_group, x="mes", y="count", 
                  color='anio',text='count', markers=True,
                  labels={'count': 'Incidencia delictiva',
                          'anio': 'Año',
                          'mes': 'Mes'},
                  height=600,
                  title='INCIDENCIA DELICTIVA '+str(age),
                  )

    fig.update_traces(textposition="bottom right")
    return fig

@callback(
    Output('graph_tab1-1', 'figure'),
    Input('age_tab1-1', 'value'),
    Input('delito_tab1-1', 'value')
)
def graph_delito(age, delito):
    df = data.get_data_incidentes()
    df_group = data.incidencia_delictiva(df, ['mes', 'anio', 'id_Grupo'])
    mask = (df_group['anio'].isin(age) & df_group['id_Grupo'].isin([delito]))
    df_group = df_group[mask]
    df_group = data.rellenar_meses_faltantes(df_group, age)
    df_group = data.remplazar_meses(df_group)
    
    fig = px.line(df_group, x="mes", y="count", color='anio',
                  text='count', markers=True,
                    labels={'count': 'Incidencia delictiva',
                            'anio': 'Año',
                            'mes': 'Mes'},
                    height=600,
                    title=delito+' '+str(age),
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
    df = data.get_data_incidentes()
    df_group = data.incidencia_delictiva(df, ['descripcion', 'id_Grupo', 'anio', 'mes'])
    mask = (df_group['anio'].isin(age) & df_group['descripcion'].isin([distrito]) & df_group['id_Grupo'].isin([delito]))
    df_group = df_group[mask]
    df_group = data.rellenar_meses_faltantes(df_group, age)
    df_group = data.remplazar_meses(df_group)
    
    fig = px.line(df_group, x="mes", y="count", color='anio', 
                  text='count', markers=True,
                    labels={'count': 'Incidencia delictiva',
                            'anio': 'Año',
                            'mes': 'Mes'},
                    title=delito+' EN '+distrito+' '+str(age),
                  )
                  
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
    
    df = data.get_data_incidentes()
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
    Input('sectores_tab3', 'value'),
    Input('delito_tab3', 'value'),
    Input('limites-sector', 'value')
)
def graph_map(sectores, delito, limites_sector):    
    distritos_df = data_graph.get_distritos()
    
    if delito is str:
        aux = [delito]
    else:
        aux = delito
    
    fig = px.choropleth_mapbox(distritos_df,
                            geojson=distritos_df.geometry,
                            locations=sectores,
                            color=sectores,
                            color_discrete_map={
                                'ORIENTE': '#96B6C5',
                                'PONIENTE': '#ADC4CE',
                                'CENTRO': '#EEE0C9',
                                'RIVERAS': '#FFDDCC',
                                'VALLE': '#FFDDCC',
                                'SUR': '#FFCCCC',
                                'UNIVERSIDAD': '#FEBBCC',
                            },
                            mapbox_style='open-street-map',
                            zoom=10.5,
                            center={"lat": 31.65, "lon": -106.48333},    
                            opacity=0.5,
                            height=600,
                            )
    if limites_sector != None:
        for sector in sectores:
            data_graph.get_sectores(fig, sector)

    
    for item in aux:
        data_graph.get_calles(fig, item, sectores)        
    
        
    fig.update_layout(
        title='Incidencia delictiva en '+str(sectores),
        autosize=True,
        margin={"r":0,"t":0,"l":0,"b":0},
    )
    
    return fig


@callback(
    Output('table_tab3', 'data'),
    Input('table_tab3', 'page_current'),
    Input('table_tab3', 'page_size'),
    Input('delito_tab3', 'value')
)
def update_table(page_current, page_size, delitos):
    df = data_graph.get_info_delito(delitos)
    df['index'] = range(1, len(df) + 1)
    df = df.sort_values(by='id_Grupo')
    
    return df.to_dict('records')
    # return df.iloc[
    #     page_current*page_size:(page_current+ 1)*page_size
    # ].to_dict('records')


if __name__ == '__main__':
    app.run(debug=True)