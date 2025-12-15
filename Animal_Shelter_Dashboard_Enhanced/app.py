import dash
from dash import dcc, html, Input, Output
import dash_leaflet as dl
import pandas as pd
import plotly.express as px
from animal_shelter import AnimalShelter

# AnimalShelter now connects to a local MySQL database instead of the
# original MongoDB instance used in CS-340.

# Initialize the app
app = dash.Dash(__name__)
server = app.server
shelter = AnimalShelter()

# Layout of the app
app.layout = html.Div([
    html.H1("Animal Shelter Dashboard", style={'textAlign': 'center'}),
    html.Img(src='assets/logo.png', style={'width': '200px'}),

    html.Div([
        html.Label("Select Animal Type:"),
        dcc.Dropdown(
            id='animal-type',
            options=[
                {'label': 'Dog', 'value': 'Dog'},
                {'label': 'Cat', 'value': 'Cat'}
            ],
            value='Dog',
            clearable=False
        ),
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Br(),

    html.Div(id='results-table', style={'width': '90%', 'margin': 'auto'}),

    dl.Map(
        id='geo-map',
        center=[30.2672, -97.7431],
        zoom=10,
        children=[dl.TileLayer()],
        style={'width': '100%', 'height': '500px', 'margin': 'auto'}
    ),

    dcc.Graph(id='breed-chart')
])


# Callback to update table, map, and chart
@app.callback(
    [Output('results-table', 'children'),
     Output('geo-map', 'children'),
     Output('breed-chart', 'figure')],
    [Input('animal-type', 'value')]
)
def update_dashboard(animal_type):
    results = shelter.read({"animal_type": animal_type})
    df = pd.DataFrame(results)

    if df.empty:
        return html.P("No matching results found."), [dl.TileLayer()], px.pie(title="Breed Distribution")

    df = df.head(10)
    df = df.drop(columns=['_id'], errors='ignore')

    table = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df.columns])),
        html.Tbody([
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))
        ])
    ], style={'border': '1px solid black', 'width': '100%', 'textAlign': 'left'})

    # Map Markers
    markers = [
        dl.Marker(
            position=[row['location_lat'], row['location_long']],
            children=dl.Tooltip(row['breed'])
        ) for _, row in df.iterrows() if 'location_lat' in row and 'location_long' in row
    ]

    map_layers = [dl.TileLayer()] + markers

    # Pie Chart
    fig = px.pie(df, names='breed', title='Breed Distribution')

    return table, map_layers, fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)  # host defaults to 127.0.0.1
