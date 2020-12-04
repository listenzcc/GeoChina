# File: app.py
# Aim: Web-based application of the GeoProject

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

from dash.dependencies import Input, Output

from GeoData.manager import Manager

app = dash.Dash(__name__)

manager = Manager()
fig = manager.draw_latest()

selector1 = dcc.Dropdown(
    id='selector1',
    options=manager.options,
    value=None
)

button1 = html.Button(
    'Up',
    id='button1',
    n_clicks=0
)

graph1 = dcc.Graph(
    figure=fig,
    id='graph1'
)

left_panel = html.Div(
    [selector1,
     button1],
    id='left-panel'
)

middle_panel = html.Div(
    [graph1],
    id='middle-panel'
)

main_area = html.Div(
    [left_panel,
     middle_panel],
    id='main-area'
)

app.layout = html.Div(
    [main_area],
    id='main-page'
)


@app.callback(
    Output('graph1', 'figure'),
    Output('selector1', 'options'),
    Input('selector1', 'value'),
    Input('button1', 'n_clicks')
)
def update1(adcode, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(changed_id)
    if 'button1' in changed_id:
        manager.fetch_parent()
        fig = manager.draw_latest()
        return fig, manager.options

    print('-----------------------------------')
    print(adcode)

    if adcode is None:
        return manager.fig, manager.options

    manager.fetch(adcode)
    fig = manager.draw_latest()
    return fig, manager.options


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
