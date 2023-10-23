from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.io as pio
import plotly.express as px

import pandas as pd
import datetime

import utils.data as data
import utils.graph as graph

TEMPLATE_LIGHT = "plotly_white"
TEMPLATE_DARK = "cyborg"

pio.templates.default = TEMPLATE_LIGHT

df = data.convinar_dataframes('./data/')
df = data.agregar_fecha(df)
now = datetime.datetime.now()

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# tab1_content = dbc.Card([
#     dbc.CardBody([
#         html.H3('Incidencia delictiva', className='card-title'),
#         dcc.Checklist(
#             id='age_incidencia',
#             options=list(df['anio'].unique()),
#             value=[now.year],
#             inline=True,
#             labelStyle={'display': 'inline-block'}
#         ),
#         dcc.Graph(id='total_graph')
#     ]),
    
#     dbc.CardBody([
#         html.H3('Incidencia delictiva por delito', className='card-title'),
#         dcc.Checklist(
#             id='age_delito',
#             options=list(df['anio'].unique()),
#             value=[now.year-1,now.year],
#             inline=True,
#             labelStyle={'display': 'inline-block'}
#         ),
#         dcc.Dropdown(
#             id='delito',
#             options=list(data.remover_null_delitos(df)),
#             value='ABUSO SEXUAL'
#         ),
#         dcc.Graph(id='only_graph')
#     ])
# ])

# tab2_content = dbc.Card([
#     dbc.CardBody([
#         html.H3('Incidencia delictiva por distrito', className='card-title'),
#     ])
# ])

# tab3_content = dbc.Card([
#     dbc.CardBody([
#         html.H3('Mapas', className='card-title'),
        
#         dcc.Geolocation(id='geolocation'),
        
#     ])
# ])

# app.layout = html.Div([
#     # Tabs
#     dbc.Tabs([
#         dbc.Tab(tab1_content , label='Incidencia delictiva por año', tab_id='tab-1'),
#         dbc.Tab(tab2_content, label='Incidencia delictiva por distrito', tab_id='tab-2'),
#         dbc.Tab(tab3_content, label='Mapas', tab_id='tab-3'),
#     ]),
# ])


@callback(
    Output('total_graph', 'figure'),
    Input('age_incidencia', 'value')
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
    Output('only_graph', 'figure'),
    Input('age_delito', 'value'),
    Input('delito', 'value')
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


if __name__ == '__main__':
    app.run(debug=True)
