import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash

app = dash.Dash(__name__)

# Crear un gráfico con dos trazas
fig = make_subplots(rows=1, cols=1)

trace1 = go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode='lines', name='Trace 1')
trace2 = go.Scatter(x=[1, 2, 3], y=[7, 8, 9], mode='lines', name='Trace 2')

fig.add_trace(trace1, row=1, col=1)
fig.add_trace(trace2, row=1, col=1)

# BEGIN: 8f7a6d5b1c2e
# Crear un menú de selección múltiple que permita al usuario seleccionar qué trazas se muestran
updatemenu = []
buttons = []

# Opción para mostrar solo la traza 1
buttons.append(dict(method='update',
              label='Trace 1',
              args=[{'visible': [True, False]}],
              )
          )

# Opción para mostrar solo la traza 2
buttons.append(dict(method='update',
              label='Trace 2',
              args=[{'visible': [False, True]}],
              )
          )

# Opción para mostrar ambas trazas
buttons.append(dict(method='update',
              label='Both',   
              args=[{'visible': [True, True]}],
              )
          )

# Añadir los botones al menú
updatemenu.append(dict(active=0, buttons=buttons, direction='down', showactive=True, x=0.1, xanchor='left', y=1.1, yanchor='top'))

# Actualizar el layout del gráfico para incluir el menú
fig.update_layout(showlegend=True, updatemenus=updatemenu)
# END: 8f7a6d5b1c2e

fig.show()
if __name__ == '__main__':
    app.run_server(debug=True)