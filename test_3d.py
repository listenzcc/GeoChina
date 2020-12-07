import dash
import dash_html_components as html
import dash_core_components as dcc
import numpy as np
import plotly.graph_objs as go

from dash.dependencies import Input, Output

app = dash.Dash(__name__)

volume = np.zeros((10, 15, 20))
for a in range(3):
    for b in range(4):
        for c in range(5):
            volume[a, b, c] = 1

dim = volume.shape

slider1 = dcc.Slider(
    id='slider1',
    max=dim[0],
    min=0,
    value=0,
    step=1,
)
slider2 = dcc.Slider(
    id='slider2',
    max=dim[1],
    min=0,
    value=0,
    step=1,
)
slider3 = dcc.Slider(
    id='slider3',
    max=dim[2],
    min=0,
    value=0,
    step=1,
)

graph1 = dcc.Graph(
    id='graph1',
)

app.layout = html.Div(
    [slider1, slider2, slider3, graph1]
)


@app.callback(
    Output('graph1', 'figure'),
    Input('slider1', 'value'),
    Input('slider2', 'value'),
    Input('slider3', 'value'),
)
def update1(value1, value2, value3):
    print('----------------------------------------')
    print(volume.shape)
    print(value1, value2, value3)
    print(dim)
    xx = np.array(range(dim[0]))
    yy = np.array(range(dim[1]))
    zz = np.array(range(dim[2]))

    # trace X
    z, y = np.meshgrid(zz, yy)
    x = z * 0 + value1
    surf = volume[value1, :, :]
    tracex = go.Surface(
        x=x,
        y=y,
        z=z,
        surfacecolor=surf,
        colorscale='Gray'
    )

    # trace Y
    z, x = np.meshgrid(zz, xx)
    y = x * 0 + value2
    surf = volume[:, value2, :]
    tracey = go.Surface(
        x=x,
        y=y,
        z=z,
        surfacecolor=surf,
        colorscale='Gray'
    )

    # trace Z
    y, x = np.meshgrid(yy, xx)
    z = y * 0 + value3
    surf = volume[:, :, value3]
    print(z.shape, surf.shape)
    tracez = go.Surface(
        x=x,
        y=y,
        z=z,
        surfacecolor=surf,
        colorscale='Gray'
    )

    data = [
        tracex,
        tracey,
        tracez,
    ]
    fig = go.Figure(data=data)

    m = max(dim)
    fig.update_layout(
        title='Volume',
        scene=dict(
            xaxis={'range': [-1, dim[0]]},
            yaxis={'range': [-1, dim[1]]},
            zaxis={'range': [-1, dim[2]]},
            aspectratio=dict(x=dim[0]/m,
                             y=dim[1]/m,
                             z=dim[2]/m),
        )
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
