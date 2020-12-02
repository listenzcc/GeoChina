# File: manager.py
# Aim: Data manager of fetching-down soliding-to and checking-out geography data

import pandas as pd
import time
import urllib

from . import logger


def full_url(adcode=100000):
    # Make full URL of the [adcode]
    json_name = f'{adcode}_full.json'
    return f'https://geo.datav.aliyun.com/areas_v2/bound/{json_name}'


class Manager(object):
    def __init__(self, adcode=100000):
        logger.info('Manager initialized')

    def fetch(self, adcode):
        # Fetch .json as DataFrame of [adcode]
        t = time.time()
        url = full_url(adcode)
        try:
            frame = pd.read_json(url)
        except urllib.error.HTTPError:
            logger.error(
                f'Failed to fetch .json from: "{url}"'
            )
            return None

        cnt = len(frame)
        t = time.time() - t
        logger.debug(
            f'Fetched .json of "{adcode}", which has "{cnt}" records, costing "{t}" seconds')
        return frame

    def get_children(self, frame):
        # Get children features
        table = dict()
        for f in frame.features.to_list():
            df = pd.DataFrame(f).transpose()
            name = df.name['properties']
            if len(name) == 0:
                continue
            adcode = df.adcode['properties']
            table[name] = (adcode, name)
        return table
