# File: manager.py
# Aim: Data manager of fetching-down soliding-to and checking-out geography data

import geopandas as gpd
import json
import numpy as np
import os
import plotly.graph_objects as go
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
    # Parse the features from the [frame]
    geodf = gpd.GeoDataFrame.from_features(geojson['features']).set_index(idx)
    if '' in geodf.index:
        geodf = geodf.drop(index='')
    return geodf


def get_options(geodf):
    options = []
    for j in range(len(geodf)):
        _name = geodf.index[j]
        _adcode = geodf.adcode[_name]
        options.append(dict(label=_name,
                            value=_adcode))
    return options


def fig_factory(fig):
    fig.update_layout(
        margin=dict(
            # r=0,
            # t=0,
            # l=0,
            # b=0,
        )
    )
    return fig


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
        self.level_table = {adcode: 'country'}
        self.name_table = {adcode: '中国'}
        self.childrenNum_table = {adcode: 34.0}
        self.parent_table = {adcode: adcode}
        logger.info('Manager initialized')
        if init_fetch:
            self.fetch(adcode)

    def fetch(self, adcode):
        # Fetch geojson of [adcode]
        adcode = str(adcode)
        if self.childrenNum_table[adcode] == 0:
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
        for name in geodf.index:
            _adcode = str(geodf.adcode[name])
            self.name_table[_adcode] = name
            self.level_table[_adcode] = geodf.level[name]
            self.childrenNum_table[_adcode] = geodf.childrenNum[name]
            self.parent_table[_adcode] = str(geodf.parent[name]['adcode'])
        cnt = len(geodf)

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
        adcode = self.parent_table[self.adcode]
        self.fetch(adcode)

    def draw_latest(self):
        # Draw map of latest fetch
        colorscale = 'Viridis'
        opacity = 0.5
        centers = np.array(self.geodf.center.to_list())
        mean = centers.mean(axis=0)
        center = dict(
            lat=mean[1],
            lon=mean[0],
        )
        style = 'light'
        zoom = zoom_table.get(self.level_table[self.adcode], default_zoom)
        name = self.name_table[self.adcode]
        title = f'Choropleth Mapbox of "{name}"'
        logger.debug(f'Using zoom of: "{zoom}"')

        data = go.Choroplethmapbox(
            geojson=self.geojson,
            featureidkey='properties.name',
            locations=self.geodf.index,
            z=self.geodf.childrenNum,
            colorscale=colorscale,
            marker=dict(opacity=opacity,),
            marker_line_width=0,
        )
        fig = go.Figure(data)

        fig.update_layout(
            mapbox_accesstoken=token,
            mapbox_center=center,
            mapbox_style=style,
            mapbox_zoom=zoom,
            title=title,
            # showlegend=True,
        )

        fig = fig_factory(fig)
        self.fig = fig

        return fig
