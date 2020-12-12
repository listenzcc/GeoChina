# File: manager.py
# Aim: Data manager of fetching-down soliding-to and checking-out geography data

import geopandas as gpd
import json
import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go
import random
import time
import urllib

from urllib.request import urlopen

from . import logger

token = open(os.path.join(os.environ['onedrive'], '.mapbox_token')).read()


def full_url(adcode=100000):
    # Make full URL of the [adcode]
    json_name = f'{adcode}_full.json'
    return f'https://geo.datav.aliyun.com/areas_v2/bound/{json_name}'


def parse_geojson(geojson, idx='name'):
    # Parse the features from the [geojson]
    geodf = gpd.GeoDataFrame.from_features(geojson['features']).set_index(idx)
    if '' in geodf.index:
        geodf = geodf.drop(index='')
    return geodf


def get_options(geodf):
    # Get options of the [geodf],
    # the format is {label: {name}; value: {adcode}}
    options = []
    for j in range(len(geodf)):
        _name = geodf.index[j]
        _adcode = geodf.adcode[_name]
        options.append(dict(label=_name,
                            value=_adcode))
    return options


def fig_factory(fig):
    # Global figure factory of [fig],
    # used to set margin, padding, etc...
    fig.update_layout(
        margin=dict(
            # r=0,
            # t=0,
            # l=0,
            # b=0,
        )
    )
    return fig


def append_random_values(df, columns=['Value1', 'Value2', 'Value3']):
    def _random():
        return [random.randint(3, 13) for _ in df.index]
    for c in columns:
        df[c] = _random()
    return df


"""
At zoom level, You can see
0, The Earth
3, A continent
4, Large islands
6, Large rivers
10, Large roads
15, Buildings
"""

zoom_table = dict(
    country=3,
    province=6,
    city=8,
    district=10,
)
default_zoom = 3


class Manager(object):
    def __init__(self, init_fetch=True):
        adcode = '100000'
        known_adcode = pd.DataFrame(
            columns=['level', 'name', 'parent', 'childrenNum'])
        known_adcode = known_adcode.append(pd.Series(dict(
            level='country',
            name='中国',
            parent=adcode,
            childrenNum=34,
        ), name=adcode))
        self.known_adcode = known_adcode
        logger.info('Manager initialized')
        if init_fetch:
            self.fetch(adcode)

    def fetch(self, adcode):
        # Fetch geojson of [adcode]
        logger.debug(f'Fetching geojson of "{adcode}"')
        adcode = str(adcode)
        if self.known_adcode.childrenNum[adcode] == 0:
            logger.debug(
                f'Not fetching adcode: "{adcode}" since it has no children')
            return None, None
        # Start timing
        t = time.time()

        # Fetch geojson
        url = full_url(adcode)
        try:
            with urlopen(url) as response:
                geojson = json.load(response)
        except urllib.error.HTTPError:
            logger.error(f'Failed to fetch geojson from: "{url}"')
            return None, None

        # Parse geojson into geodf
        geodf = parse_geojson(geojson)
        cnt = len(geodf)
        append_random_values(geodf)

        # Add all records into known_adcode
        for name in geodf.index:
            _adcode = str(geodf.adcode[name])
            if _adcode in self.known_adcode.index:
                # ! Only append _adcode record ONCE
                continue
            self.known_adcode = self.known_adcode.append(pd.Series(dict(
                level=geodf.level[name],
                name=name,
                parent=str(geodf.parent[name]['adcode']),
                childrenNum=geodf.childrenNum[name],
            ), name=_adcode))

        # Report and return
        t = time.time() - t
        logger.debug(
            f'Fetched geojson of "{adcode}", which has "{cnt}" records, costing "{t}" seconds')
        print(geodf[['adcode', 'level', 'parent', 'center', 'childrenNum']])

        self.adcode = adcode
        self.geojson = geojson
        self.geodf = geodf
        self.options = get_options(geodf)
        return geojson, geodf

    def fetch_parent(self):
        adcode = self.known_adcode.parent[self.adcode]
        self.fetch(adcode)

    def draw_barchart(self, columns=['Value1', 'Value2', 'Value3']):
        # Draw columns of the geodf in bar chart
        x = self.geodf.index
        data = []
        for c in columns:
            y = self.geodf[c]
            data.append(go.Bar(
                x=x,
                y=y,
                name=c))

        layout = go.Layout(
            title='Bar chart'
        )
        fig = go.Figure(data=data, layout=layout)
        return fig

    def draw_mapbox(self, opacity=0.5, x_zoom=1, only_update_layout=False):
        # Draw map of latest fetch
        # Setup parameters
        colorscale = 'Viridis'
        opacity = opacity
        # centers of the adcode areas,
        # array of n x 2, n: areas number; 2: [longtitute, latitude]
        centers = np.array(self.geodf.center.to_list())
        # mean = centers.mean(axis=0)
        center = dict(
            lon=(max(centers[:, 0]) + min(centers[:, 0]))/2,
            lat=(max(centers[:, 1]) + min(centers[:, 1]))/2,
            # lat=mean[1],
            # lon=mean[0],
        )
        style = 'light'
        level = self.known_adcode.level[self.adcode]
        zoom = zoom_table.get(level, default_zoom)
        zoom = zoom * x_zoom
        name = self.known_adcode.name[self.adcode]
        title = f'Choropleth Mapbox of "{name} ({level})"'
        logger.debug(f'Using zoom of: "{zoom}"')

        if all([only_update_layout,
                hasattr(self, 'fig')]):
            fig = self.fig
            fig['data'][0]['marker']['opacity'] = opacity
        else:
            # Setup data for Choroplethmapbox
            data = go.Choroplethmapbox(
                geojson=self.geojson,
                featureidkey='properties.name',
                locations=self.geodf.index,
                z=self.geodf.childrenNum,
                colorscale=colorscale,
                marker=dict(opacity=opacity,),
                marker_line_width=0,
            )

            # Add data into fig
            fig = go.Figure(data)

        # Update the layout of the fig
        fig.update_layout(
            mapbox_accesstoken=token,
            mapbox_center=center,
            mapbox_style=style,
            mapbox_zoom=zoom,
            title=title,
            uirevision='constant',
            # showlegend=True,
        )

        fig = fig_factory(fig)
        self.fig = fig

        return fig
