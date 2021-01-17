# Data Worker

# %%
import os
import pandas as pd
import plotly.express as px
from pypinyin import lazy_pinyin

locations_url = 'https://blog.csdn.net/envbox/article/details/80290103'
filename = 'locations.json'
sync_folder = os.environ.get('Sync', '.')
mapbox = dict(
    mapbox_accesstoken=open(os.path.join(
        os.environ['onedrive'], '.mapbox_token')).read(),
    mapbox_style='light'
)


def fetch_locations():
    locations = pd.read_html(locations_url)[0]
    locations.columns = ['Province', 'ID', 'Name',
                         'Latitude', 'Longitude', 'Height']
    # Fix Known Issue,
    # use height - 10000 if height is greater than 10000
    locations.Height = locations.Height.map(lambda e: e % 10000)

    def translate(s):
        return ''.join(lazy_pinyin(s))

    locations['_province'] = locations['Province'].map(translate)
    locations['_name'] = locations['Name'].map(translate)
    locations = locations[['ID', 'Province', 'Name',
                           'Latitude', 'Longitude', 'Height',
                           '_province', '_name']]
    return locations


class DataWorker(object):
    def __init__(self):
        self.locations = fetch_locations()
        self.columns = self.locations.columns
        self.plot_mapbox(self.locations.copy())

    def search_by_pinyin(self, py):
        found = dict()
        if py.strip() == '':
            found['_name'] = self.locations.copy()
            found['_province'] = pd.DataFrame()
        else:
            for col in ['_province', '_name']:
                found[col] = self.locations[self.locations[col].str.startswith(
                    py)]

        output = pd.concat([found['_name'], found['_province']], axis=0)
        self.plot_mapbox(output.copy())

        return output

    def plot_mapbox(self, df):
        print('Reploting')
        df['ID'] = df['ID'].map(str)
        df['Text'] = df[['Province', 'Name', 'ID']].apply(', '.join, axis=1)
        fig = px.scatter_mapbox(
            df,
            lon='Longitude',
            lat='Latitude',
            color='Province',
            #     size=3,
            hover_name='Text',
            zoom=2,
            height=300
        )
        fig.update_layout(**mapbox)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        self.canvas = fig.to_html()

        return self.canvas

# %%
# dw = DataWorker()
# dw.locations

# %%
# dw.search_by_pinyin('bei')
