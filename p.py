import folium
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import webbrowser


#se lee el archivo csv
capitales = pd.read_csv("europa.csv")

# Crear el mapa de Folium
m = folium.Map(location=[52, 20], zoom_start=4.3)

#creamos un marcador para cada ciudad
for i, row in capitales.iterrows():
    folium.Marker(location=[row["Latitud"], row["Longitud"]], 
                  popup=row["Capital"]).add_to(m)

# Crear la aplicación Dash
app = dash.Dash(__name__)
  
@app.callback(
    Output('selected-markers-list', 'children'),
    [Input('selected-markers', 'data')]
)
def update_selected_markers_list(selected_markers):
    if selected_markers:
        return [html.Li(marker['popup']) for marker in selected_markers]
    else:
        return "No hay marcadores seleccionados"





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
