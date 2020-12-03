# File: app.py
# Aim: Web-based application of the GeoProject

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

from dash.dependencies import Input, Output

from GeoData.manager import Manager

app = dash.Dash(__name__)
adcode = 100000

manager = Manager()
_, geodf = manager.fetch(adcode=adcode)
fig = manager.draw_latest()

controller = dcc.Dropdown(
    id='controller',
    options=manager.options,
    value=adcode
)

graph = dcc.Graph(
    figure=fig,
    id='graph'
)

app.layout = html.Div([
    html.Div(
        [controller],
        id='control-area'),
    html.Div(
        [graph],
        id='graph-area')
])


@app.callback(
    Output('graph', 'figure'),
    Output('controller', 'options'),
    Input('controller', 'value'),
)
def update_output(adcode):
    print('-----------------------------------')
    print(adcode)
    manager.fetch(adcode)
    fig = manager.draw_latest()

    return fig, manager.options


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
