from dash import callback, Output, Input
import plotly.express as px
import pandas as pd

import utils.data as data

# @callback(
#     Output('total_graph', 'figure'),
#     Input('age_incidencia', 'value')
# )
def graph_age(age, df):
    df_group = data.incidencia_delictiva(df)
    mask = df_group['anio'].isin(age)
    df_group = df_group[mask]
    df_group = data.rellenar_meses_faltantes(df_group, age)
    df_group = data.remplazar_meses(df_group)
    
    # import pdb; pdb.set_trace()
    fig = px.line(df_group, x="mes", y="count", color='anio',text='count', markers=True)
    fig.update_traces(textposition="bottom right")
    return fig