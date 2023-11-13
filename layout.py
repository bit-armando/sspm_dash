from dash import html, dcc
import dash_bootstrap_components as dbc

import datetime
import os

import utils.data as data

df = data.convinar_dataframes([2022,2023])
now = datetime.datetime.now()

age = [x for x in os.listdir('./data/')]
age = [int(x.replace('.csv', '')) for x in age]

tab1_content = dbc.Card([
    dbc.Row([
        dbc.Col([
            dbc.CardBody([
                dbc.Col([html.H1('Incidencia delictiva', className='text-center text-secondary')]),
                
                dcc.Checklist(
                    id='age_tab1',
                    options=age,
                    value=[now.year, now.year-1],
                    inline=True,
                    labelStyle={'display': 'inline-block'},
                    className='list-group-item'
                ),
            ]),
        ]),
    ]),
    
    dbc.Row([
        dbc.CardBody([
            dcc.Graph(id='graph_tab1')
        ]),
    ]),
    
    dbc.Row([
        dbc.CardBody([
            dbc.Col(html.H1('Incidencia delictiva por delito', className='text-center text-secondary')),
            dcc.Checklist(
                id='age_tab1-1',
                options=age,
                value=[now.year-1,now.year],
                inline=True,
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Dropdown(
                id='delito_tab1-1',
                # options=list(data.remover_null_delitos(df)),
                options=df['id_Grupo'].unique(),
                value='ABUSO SEXUAL'
            ),
            dcc.Graph(id='graph_tab1-1')
        ]),
    ])
], class_name='card')

tab2_content = dbc.Card([
    dbc.Row([
        dbc.Col([
            dbc.CardBody([
                html.H1('Incidencia delictiva por distrito', className='text-center text-secondary'),
                dcc.Checklist(
                    id='age_tab2',
                    options=age,
                    value=[now.year, now.year-1],
                    inline=True,
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.Dropdown(
                    id='distrito_tab2',
                    options=list(df['descripcion'].unique()),
                    value='CENTRO'
                ),
                dcc.Dropdown(
                    id='delito_tab2',
                    options=df['id_Grupo'].unique(),
                    value='ARMAS DECOMISADAS'
                ),
            ]),
        ],width=3),
        dbc.Col([
            dcc.Graph(id='graph_tab2')
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.CardBody([
                html.H1('Incidencia delictiva por mes', className='text-center text-secondary'),
                dcc.Checklist(
                    id='age_tab2-2',
                    options=age,
                    value=[now.year, now.year-1],
                    inline=True,
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.Dropdown(
                    id='delito_tab2-2',
                    options=df['id_Grupo'].unique(),
                    value='ARMAS DECOMISADAS'
                ),
                dcc.Dropdown(
                    id='Mes_tab2-2',
                    options=list(sorted(df['id_fecha'].dt.month.unique())),
                    value=now.month
                ),
            ]),
        ], width=3),
        dbc.Col([
            dcc.Graph(id='graph_tab2-2')
        ])
    ])
], class_name='card')

distritos = ['CENTRO', 'UNIVERSIDAD', 'ORIENTE', 'VALLE', 'PONIENTE', 'SUR', 'RIVERAS']

tab3_content = dbc.Card([
    dbc.CardBody([
        html.H3('Mapas', className='card-title'),
        dcc.RadioItems(
            id='age_tab3',
            options=age,
            value=now.year,
            inline=True,
            labelStyle={'display': 'inline-block'}
        ),
        
        dcc.Dropdown(
            id='delito_tab3',
            options=df['id_Grupo'].unique(),
            value='',
            multi=True
        ),
        
        dcc.Dropdown(
            id='sectores_tab3',
            options=distritos,
            value=['SUR'],
            multi=True
        ),
        dcc.Graph(id='graph_tab3'),
        
    ])
], class_name='card')

layout = dbc.Container([
    # Tabs
    dbc.Tabs([
        dbc.Tab(tab1_content , label='Incidencia delictiva por año', tab_id='tab-1'),
        dbc.Tab(tab2_content, label='Incidencia delictiva por distrito', tab_id='tab-2'),
        dbc.Tab(tab3_content, label='Mapas', tab_id='tab-3'),
    ]),
], class_name='container-fluid')