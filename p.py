import folium
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State

import webbrowser


# Crear la aplicación Dash
app = dash.Dash(__name__)

# Crear el mapa de Folium
m = folium.Map(location=[54.5260, 15.2551], zoom_start=4)

# Añadir un marcador en Madrid, España
madrid_marker = folium.Marker(location=[40.4168, -3.7038], tooltip="Madrid, España", customdata="Madrid")
madrid_marker.add_to(m)

# Añadir un marcador en París, Francia
paris_marker = folium.Marker(location=[48.8566, 2.3522], tooltip="París, Francia", customdata="Paris")
paris_marker.add_to(m)

# Añadir un marcador en Berlín, Alemania
berlin_marker = folium.Marker(location=[52.5200, 13.4050], tooltip="Berlín, Alemania", customdata="Berlin")
berlin_marker.add_to(m)

# Convertir el mapa de Folium en un objeto HTML
html_map = m._repr_html_()

# Definir el diseño de la aplicación Dash
app.layout = html.Div([
    html.H1("Mapa de Europa"),
    dcc.Graph(id='map', figure=m._repr_html_()),
    #html.Iframe(id='map', srcDoc=html_map, width='100%', height='600'),
    html.Label("Marcadores seleccionados:"),
    dcc.Store(id='selected-markers', data=[]),
    html.Ul(id='selected-markers-list'),
    html.Label(id='selected-markers-label')
])


# Crear una función para actualizar la lista de marcadores seleccionados y el textlabel
@app.callback(
    [Output('selected-markers', 'data'), Output('selected-markers-label', 'children'), Output('selected-markers-list', 'children')],
    Input('map', 'clickData'),
    State('selected-markers', 'data')
)
def update_selected_markers(clickData, selected_markers):
    if clickData is not None:
        tooltip = clickData['points'][0]['customdata']
        #tooltip = clickData['points'][0]['tooltip']
        selected_markers.append(tooltip)
        label = "Marcador seleccionado: " + tooltip
        list_items = [html.Li(marker) for marker in selected_markers]
        return selected_markers, label, list_items
    else:
        label = "Selecciona un marcador en el mapa"
        return selected_markers, label, []
if __name__ == '__main__':
    # Abrir el navegador con la aplicación Dash
    webbrowser.open('http://127.0.0.1:8050/')
    # Ejecutar la aplicación Dash
    app.run_server(debug=True)
