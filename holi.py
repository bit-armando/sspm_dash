import plotly.graph_objects as go

fig = go.Figure(go.Scattermapbox(
    lat=['45.5017'],
    lon=['-73.5673'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=14
    ),
    text=["Texto de ejemplo"],  # Aquí es donde agregas el texto
))

fig.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        bearing=0,
        center=dict(
            lat=45,
            lon=-73
        ),
        pitch=0,
        zoom=10
    ),
)

fig.show()