from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from flask import Flask

app = Flask(__name__)

fig = px.line(
    x=["a","b","c"], y=[1,3,2], # replace with your own data source
    title="sample figure", height=325
)

@app.route('/')
def index():

    return 'Hello Flask app'

@app.route('/plot')
# @app.callback(
#     Output("graph", "figure"), 
#     Input("dropdown", "value"))
def plot(dims):
    app.layout = html.Div([
        html.H4('Analysis of Iris data using scatter matrix'),
        dcc.Dropdown(
            id="dropdown",
            options=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
            value=['sepal_length', 'sepal_width'],
            multi=True
        ),
        dcc.Graph(id="graph"),
    ])
    
    df = px.data.iris() # replace with your own data source
    fig = px.scatter_matrix(df, dimensions=dims, color="species")
    return fig

if __name__ == '__main__':
    app.run(debug=True)
