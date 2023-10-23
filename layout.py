import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import pandas as pd

tab1_content = dbc.Card([
    dbc.CardBody([
        html.H3('Incidencia delictiva', className='card-title'),
        dcc.Checklist(
            id='age_incidencia',
            options=list(df['anio'].unique()),
            value=[now.year],
            inline=True,
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id='total_graph')
    ]),
    
    dbc.CardBody([
        html.H3('Incidencia delictiva por delito', className='card-title'),
        dcc.Checklist(
            id='age_delito',
            options=list(df['anio'].unique()),
            value=[now.year-1,now.year],
            inline=True,
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='delito',
            options=list(data.remover_null_delitos(df)),
            value='ABUSO SEXUAL'
        ),
        dcc.Graph(id='only_graph')
    ])
])

tab2_content = dbc.Card([
    dbc.CardBody([
        html.H3('Incidencia delictiva por distrito', className='card-title'),
    ])
])

tab3_content = dbc.Card([
    dbc.CardBody([
        html.H3('Mapas', className='card-title'),
        
        dcc.Geolocation(id='geolocation'),
        
    ])
])

layout = html.Div([
    # Tabs
    dbc.Tabs([
        dbc.Tab(tab1_content , label='Incidencia delictiva por año', tab_id='tab-1'),
        dbc.Tab(tab2_content, label='Incidencia delictiva por distrito', tab_id='tab-2'),
        dbc.Tab(tab3_content, label='Mapas', tab_id='tab-3'),
    ]),
])