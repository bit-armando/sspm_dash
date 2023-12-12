from dash import html, dcc
from dash import dash_table
import dash_bootstrap_components as dbc
import datetime

import utils.data as data

df = data.get_data_incidentes()
now = datetime.datetime.now()

age = df['anio'].unique()

tab_document = dbc.Card([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
    ),
    html.Div(id='output-data-upload'),
])

tab1_content = dbc.Card([
    dbc.Row([
        dbc.Col([
            dbc.CardBody([
                dbc.Col([html.H1('Incidencia delictiva', className='text-center text-secondary')]),
                
                dcc.Checklist(
                    id='age_tab1',
                    options=age,
                    value=[],
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
                value=[],
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
                    value=[],
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
                    value=[],
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
        dcc.Checklist(
            id='limites-sector',
            options=['Mostrar limites de sectores'],
        ),
                
        dcc.Dropdown(
            id='delito_tab3',
            options=df['id_Grupo'].unique(),
            value=[''],
            multi=True
        ),
        
        dcc.Checklist(
            id='sectores_tab3',
            options=distritos,
            value=['SUR'],
            inline=True,
        ),
        

        dcc.Graph(id='graph_tab3'),
        
        dash_table.DataTable(
            id='table_tab3',
            columns=[{'name': i, 'id': i} for i in ['descripcion', 'id_Grupo', 'counts']],
            page_action='custom',
        )
        
    ])
], class_name='card')

layout = dbc.Container([
    # Tabs
    dbc.Tabs([
        dbc.Tab(tab_document, label='Documentos', tab_id='tab-0'),
        dbc.Tab(tab1_content , label='Incidencia delictiva por año', tab_id='tab-1'),
        dbc.Tab(tab2_content, label='Incidencia delictiva por distrito', tab_id='tab-2'),
        dbc.Tab(tab3_content, label='Mapas', tab_id='tab-3'),
    ]),
], class_name='container-fluid')