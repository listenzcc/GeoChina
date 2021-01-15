# Data Worker

# %%
import os
import pandas as pd
from pypinyin import lazy_pinyin

locations_url = 'https://blog.csdn.net/envbox/article/details/80290103'
filename = 'locations.json'
sync_folder = os.environ.get('Sync', '.')


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

    def search_by_pinyin(self, py):
        found = dict()
        for col in ['_province', '_name']:
            found[col] = self.locations[self.locations[col].str.startswith(py)]
        return pd.concat([found['_name'], found['_province']], axis=0)


# %%
# dw = DataWorker()
# dw.locations

# %%
# dw.search_by_pinyin('bei')
