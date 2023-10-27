from dash import html, dcc
import dash_bootstrap_components as dbc

import datetime

import utils.data as data

df = data.convinar_dataframes('./data/')
df = data.agregar_fecha(df)
now = datetime.datetime.now()

tab1_content = dbc.Card([
    dbc.Row([
        dbc.Col([
            dbc.CardBody([
                dbc.Col([html.H1('Incidencia delictiva', className='text-center text-secondary')]),
                
                dcc.Checklist(
                    id='age_tab1',
                    options=list(df['anio'].unique()),
                    value=[now.year],
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
                options=list(df['anio'].unique()),
                value=[now.year-1,now.year],
                inline=True,
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Dropdown(
                id='delito_tab1-1',
                options=list(data.remover_null_delitos(df)),
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
                    options=list(df['anio'].unique()),
                    value=[now.year],
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
                    options=list(data.remover_null_delitos(df)),
                    value='ABUSO SEXUAL'
                ),
            ]),
        ],width=3),
        dbc.Col([
            html.H6(id='output_tab2'),
            dcc.Graph(id='graph_tab2')
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.CardBody([
                html.H1('Incidencia delictiva por mes', className='text-center text-secondary'),
                dcc.Checklist(
                    id='age_tab2-2',
                    options=list(df['anio'].unique()),
                    value=[now.year],
                    inline=True,
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.Dropdown(
                    id='delito_tab2-2',
                    options=list(data.remover_null_delitos(df)),
                    value='ABUSO SEXUAL'
                ),
                dcc.Dropdown(
                    id='Mes_tab2-2',
                    options=list(sorted(df['mes'].unique())),
                    value='ENERO'
                ),
            ]),
        ], width=3),
    ])
], class_name='card')

tab3_content = dbc.Card([
    dbc.CardBody([
        html.H3('Mapas', className='card-title'),
        dcc.Checklist(
            id='age_tab3',
            options=list(df['anio'].unique()),
            value=[now.year],
            inline=True,
            labelStyle={'display': 'inline-block'}
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