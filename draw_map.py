# %%
import plotly.graph_objects as go
from urllib.request import urlopen
import geopandas as gpd
import json
import os
import pandas as pd

import plotly.express as px
import plotly.graph_objs as go

token = open(os.path.join(os.environ['onedrive'], '.mapbox_token')).read()

# %%
path = os.path.join('..', '..', 'Downloads', '全国.json')
geojson = json.load(open(path, 'rb'))
geo_df = gpd.GeoDataFrame.from_features(geojson['features']).set_index('name')
# display(geo_df)

df = pd.DataFrame()
df['Province'] = ['北京市', '天津市']
df['Value'] = [1, 2]


# %%
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson,
    featureidkey='properties.name',
    locations=df.Province,
    z=df.Value,
    colorscale="Viridis",
    marker=dict(
        opacity=0.5,
    ),
    zmin=0,
    zmax=3,
    marker_line_width=0))

fig.update_layout(
    mapbox_style="light",
    mapbox_accesstoken=token,
    # fitbounds='locations',
    mapbox_zoom=3,
    mapbox_center={"lat": 39.9, "lon": 116.4}
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()

# %%

fig = px.choropleth_mapbox(geo_df,
                           geojson=geo_df.geometry,
                           locations=geo_df.index,
                           color="childrenNum",
                           opacity=0.5,
                           center={"lat": 39.9, "lon": 116.4},
                           mapbox_style="open-street-map",
                           zoom=3)
fig.show()

# %%
geo_df
# %%

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
# %%
help(go.Choroplethmapbox)
# %%
