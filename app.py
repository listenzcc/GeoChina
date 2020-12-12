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
    'Level-Up',
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

slider2 = dcc.Slider(
    id='slider2',
    max=6,
    min=0,
    value=3,
    step=1,
    marks={
        0: {'label': 'x-3'},
        1: {'label': 'x-2'},
        2: {'label': 'x-1'},
        3: {'label': 'x0'},
        4: {'label': 'x1'},
        5: {'label': 'x2'},
        6: {'label': 'x3'},
    }
)

graph1 = dcc.Graph(
    # figure=manager.fig,
    id='graph1',
)

graph2 = dcc.Graph(
    id='graph2'
)

# ---------------------------------------
# Layout
left_panel = html.Div(
    [selector1,
     button1,
     slider1,
     slider2],
    id='left-panel'
)

middle_panel = html.Div(
    [graph1,
     graph2],
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
    Output('graph2', 'figure'),
    Output('selector1', 'options'),
    Input('selector1', 'value'),
    Input('button1', 'n_clicks'),
    Input('slider1', 'value'),
    Input('slider2', 'value'),
)
def update1(adcode, n_clicks, opacity_value, x_zoom_value):
    print('-----------------------------------')
    # Get triggered callback context
    prop_id, _ = latest_changed()
    kwargs = dict(
        opacity=opacity_value / 100,
        x_zoom=1.2 ** (3-x_zoom_value)
    )
    print(kwargs)

    output = dict(
        graph1=None,
        graph2=None,
        selector1=manager.options
    )
    # Update graph1 and selector1 if button1 is clicked
    # Move upward to the parent adcode
    if prop_id.startswith('button1.'):
        manager.fetch_parent()
        manager.draw_mapbox(**kwargs)
        output['graph1'] = manager.fig

    # Update graph1 and selector1 if selector1 changes
    # Selection of new adcode,
    # ! adcode is None refers NO valid selection
    if prop_id.startswith('selector1.'):
        if adcode is not None:
            manager.fetch(adcode)
            manager.draw_mapbox(**kwargs)
            output['graph1'] = manager.fig

    # Update graph1 if slider1 changes
    # Change opacity of the fig
    if any([prop_id.startswith('slider1.'),
            prop_id.startswith('slider2.')]):
        manager.draw_mapbox(only_update_layout=True,
                            **kwargs)
        output['graph1'] = manager.fig

    # Default returns of the callback
    if output['graph1'] is None:
        if not hasattr(manager, 'fig'):
            manager.draw_mapbox(**kwargs)
        output['graph1'] = manager.fig

    output['selector1'] = manager.options
    output['graph2'] = manager.draw_barchart()

    return output['graph1'], output['graph2'], output['selector1']


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
