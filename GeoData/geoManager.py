# Geo Data Manager

import os
import pandas as pd
from pypinyin import lazy_pinyin
from tqdm.auto import tqdm

local_dir = os.path.join(os.environ['Sync'], 'GeoData')


def get(e, key='adcode'):
    if isinstance(e, dict):
        return e.get(key, 0)
    return 0


def translate(s):
    return ''.join(lazy_pinyin(s))


class Manager(object):
    def __init__(self):
        main_frame = pd.read_json(os.path.join(local_dir, 'main.json'))
        main_frame.parent = main_frame.parent.map(get)
        main_frame['pinyin'] = main_frame.name.map(translate)
        self.frame = main_frame

    def query(self, expr, to_series=True):
        found = self.frame.query(expr)
        print(f'Got {len(found)} records')

        if to_series:
            if len(found) == 0:
                print(
                    f'Got ZERO records of "{expr}", but series is required, using None for return')
                return None
            if len(found) > 1:
                print(
                    f'Got MULTIPLE({len(found)}) records of "{expr}", but series is required, using the first one for return')
                return found.iloc[0]
            if len(found) == 1:
                return found.iloc[0]

        return found

    def trace(self, i):
        # Get the trace of the [i],
        # [i] refers the index in the [main_frame]
        se = self.frame.iloc[i]
        adcode = se['adcode']
        acroutes = se['acroutes']

        df = pd.DataFrame()
        for j in acroutes:
            df = df.append(self.query(f'adcode == {j}'))

        df = df.append(se)

        df = pd.concat(
            [df, self.query(f'parent == {adcode}', to_series=False)])

        return df


manager = Manager()
print(manager.frame)
print(manager.trace(33))
