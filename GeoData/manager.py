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


"""
At zoom level	You can see
0	The Earth
3	A continent
4	Large islands
6	Large rivers
10	Large roads
15	Buildings
"""

zoom_table = dict(
    country=3,
    province=6,
    city=8,
    district=10,
)


class Manager(object):
    def __init__(self, adcode=100000):
        self.level_table = dict()
        self.level_table[adcode] = 'country'
        logger.info('Manager initialized')

    def fetch(self, adcode):
        # Fetch geojson of [adcode]
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
        for j in range(len(geodf)):
            se = geodf.iloc[j]
            self.level_table[int(se['adcode'])] = se['level']
        cnt = len(geodf)

        # Report and return
        t = time.time() - t
        logger.debug(
            f'Fetched geojson of "{adcode}", which has "{cnt}" records, costing "{t}" seconds')
        self.adcode = adcode
        self.geojson = geojson
        self.geodf = geodf
        return geojson, geodf

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
        zoom = zoom_table.get(self.level_table[self.adcode], 3)
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
        print(data)
        fig = go.Figure(data)

        fig.update_layout(
            mapbox_accesstoken=token,
            mapbox_center=center,
            mapbox_style=style,
            mapbox_zoom=zoom,
        )

        fig.update_layout(
            margin=dict(
                r=0,
                t=0,
                l=0,
                b=0,
            )
        )

        return fig
