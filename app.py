import folium
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import webbrowser
from folium.plugins import FastMarkerCluster, FeatureGroupSubGroup


# Se lee el archivo csv
capitales = pd.read_csv("europa.csv")

# Crear el mapa de Folium con un fondo oscuro
m = folium.Map(location=[52, 20], zoom_start=4.3, tiles='CartoDB dark_matter')

# Crear un grupo para los marcadores
marker_group = folium.FeatureGroup(name='Capitales')

# Crear los marcadores con forma de círculo
for i, row in capitales.iterrows():
    # Se establece el color del marcador como gris
    color = 'gray'
    folium.CircleMarker(location=[row["Latitud"], row["Longitud"]], 
                        radius=5,
                        color=color,
                        fill=True,
                        fill_color=color,
                        popup=row["Capital"]).add_to(marker_group)

# Función que se llama cuando se hace clic en un marcador
def on_marker_click(feature, layer):
    # Se cambia el color del marcador a rojo
    layer.feature.properties['marker-color'] = 'red'
    layer.setIcon(folium.Icon(color='red'))
    # Se agrega el id del marcador a la lista de marcadores seleccionados
    selected_markers = dcc.Store(id='selected-markers', data=[])
    selected_markers.data.append(feature.id)
    # Se actualiza el contenido del label que muestra los marcadores seleccionados
    selected_markers_label = html.Label(id='selected-markers-label', children=f'Marcadores seleccionados: {", ".join(selected_markers.data)}')
    return [selected_markers, selected_markers_label]

# Se añade la función on_marker_click como manejador de eventos para cada marcador
for i, row in capitales.iterrows():
    marker = folium.CircleMarker(location=[row["Latitud"], row["Longitud"]], 
                                 radius=5,
                                 color='gray',
                                 fill=True,
                                 fill_color='gray',
                                 popup=row["Capital"])
    marker.add_to(marker_group)
    marker.on('click', on_marker_click)

# Añadir el grupo de marcadores al mapa
marker_group.add_to(m)

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Convertir el mapa de Folium en un objeto HTML
html_map = m._repr_html_()

# Definir el diseño de la aplicación Dash
app.layout = html.Div([
    html.H1("Mapa de Europa"),
    html.Iframe(id='map', srcDoc=html_map, width='100%', height='700'),
    html.Label("Marcadores seleccionados:"),
    dcc.Store(id='selected-markers', data=[]),
    html.Ul(id='selected-markers-list'),
    html.Label(id='selected-markers-label')
])

if __name__ == '__main__':
    # Abrir el navegador con la aplicación Dash
    webbrowser.open('http://127.0.0.1:8050/')
    # Ejecutar la aplicación Dash
    app.run_server(debug=True)
