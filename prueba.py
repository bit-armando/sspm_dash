from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly.express as px

import pandas as pd
import datetime

from utils.data import incidencia_delictiva, convinar_dataframes

df = convinar_dataframes('./data/')
df_group = incidencia_delictiva(df)
now = datetime.datetime.now()

app = Dash(__name__)




app.layout = html.Div([
    html.H1('Incidencia delictiva'),
    html.Hr(),
    
    dcc.Checklist(
        id='age',
        options=list(df_group['anio'].unique()),
        value=[now.year], # Borrar 2022 solo es de prueba
        inline=True
    ),
    
    dcc.Graph(id='graph'),
    # dash_table.DataTable(data=df_group.to_dict('records'))
])

@callback(
    Output('graph', 'figure'),
    Input('age', 'value')
)
def update_graph(age):
    df_group = incidencia_delictiva(df)
    mask = df_group['anio'].isin(age)
    
    fig = px.line(df_group[mask], x="mes", y="count", color='anio', text='count', markers=True)
    fig.update_traces(textposition="bottom right")
    return fig


if __name__ == '__main__':
    app.run(debug=True)
