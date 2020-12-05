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
# manager.draw_latest()

# ---------------------------------------
# Components
selector1 = dcc.Dropdown(
    id='selector1',
    options=[],
    value=None
)

button1 = html.Button(
    'Up',
    id='button1',
    n_clicks=0,
)

slider1 = dcc.Slider(
    id='slider1',
    max=100,
    min=0,
    value=50,
    step=10,
    marks={
        0: {'label': '0.0'},
        50: {'label': '0.5'},
        100: {'label': '1.0'},
    },
)

graph1 = dcc.Graph(
    # figure=manager.fig,
    id='graph1'
)

# ---------------------------------------
# Layout
left_panel = html.Div(
    [selector1,
     button1,
     slider1],
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

# ---------------------------------------
# Callbacks


def latest_changed():
    # Get latest changed context
    context = [e for e in dash.callback_context.triggered][0]
    prop_id = context['prop_id']
    value = context['value']
    print(
        f'Latest prop_id is "{prop_id}" with value of "{value}"')
    return prop_id, value


@app.callback(
    Output('graph1', 'figure'),
    Output('selector1', 'options'),
    Input('selector1', 'value'),
    Input('button1', 'n_clicks'),
    Input('slider1', 'value'),
)
def update1(adcode, n_clicks, opacity_value):
    print('-----------------------------------')
    # Get triggered callback context
    prop_id, _ = latest_changed()

    # Update graph1 and selector1 if button1 is clicked
    # Move upward to the parent adcode
    if prop_id.startswith('button1.'):
        manager.fetch_parent()
        fig = manager.draw_mapbox()
        return fig, manager.options

    # Update graph1 and selector1 if selector1 changes
    # Selection of new adcode,
    # !adcode is None refers NO valid selection
    if prop_id.startswith('selector1.'):
        if adcode is not None:
            manager.fetch(adcode)
            fig = manager.draw_mapbox()
            return fig, manager.options

    # Update graph1 if slider1 changes
    # Change opacity of the fig
    if prop_id.startswith('slider1.'):
        opacity = opacity_value / 100
        manager.draw_mapbox(opacity=opacity)
        return manager.fig, manager.options

    # Default returns of the callback
    if not hasattr(manager, 'fig'):
        manager.draw_mapbox()
    return manager.fig, manager.options


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
