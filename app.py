import dash
import dash_leaflet as dl
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import webbrowser

app = dash.Dash(__name__)

capitales= pd.read_csv('europa.csv')
locations = []
for i, row in capitales.iterrows():
    locations.append((row["Latitud"], row["Longitud"]))

markers = [dl.CircleMarker(id=f"marker-{i}", center=location, radius=7) for i, location in enumerate(locations)]

app.layout = html.Div([
    dl.Map(center=(52, 20), zoom=4.3, children=[
        dl.TileLayer(style={'background-color': 'gray'}),
        *markers
    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
    html.Div(id="output")
])

@app.callback(
    [Output(f"marker-{i}", "color") for i in range(len(locations))] + [Output("output", "children")],
    [Input(f"marker-{i}", "n_clicks") for i in range(len(locations))]
)
def handle_click(*args):
    colors = []
    selecteds = []
    for i, n_clicks in enumerate(args):
        if n_clicks is None or n_clicks % 2 == 0:
            colors.append("black")
        else:
            colors.append("green")
            selecteds.append(f"Marker {i}")
    return colors + [f"Selecteds: {', '.join(selecteds)}"]

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=True)
