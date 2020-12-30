# Download temperature dataset from website

# %%
import logging
import os
import pandas as pd
import requests
import traceback

from tqdm.auto import tqdm
# %%
project_name = 'download_dataset'
sync_folder = os.path.join(os.environ['HOME'], 'documents', 'Sync-Folder')
data_folder_name = 'Temperature-DataSet'
logging_format = '%(asctime)s %(levelname)s: %(message)s'
logging_level = logging.DEBUG
logging_handler = logging.StreamHandler()
logging_handler = logging.FileHandler('log.log')

# %%
# Setup logger
logger = logging.getLogger(project_name)
logger.setLevel(logging_level)
handler = logging_handler
formatter = logging.Formatter(logging_format)
handler.setFormatter(formatter)
handler.setLevel(logging_level)
if not logger.handlers:
    logger.addHandler(handler)

# Setup data_folder
assert(os.path.exists(sync_folder))
data_folder = os.path.join(sync_folder, data_folder_name)
if not os.path.exists(data_folder):
    os.mkdir(data_folder)


# %%
# Read DataFrame of stations
stations = pd.read_json('locations.json')
logger.info(f'Read {len(stations)} stations')
stations

# %%


def fetch_data(ID, year, refetch_empty=False):
    # Fetch data based on [ID] and [year],
    # use the file on the disk firstly, if exists, use it,
    # if the DataFrame on the disk is empty and refetch_empty is True,
    # try to refetch it.
    template_url = 'http://data.sheshiyuanyi.com/WeatherData/datafile/{ID}-{ID}_avg_tem_{year}_0.xlsx'
    name = os.path.basename(template_url.format(ID=ID, year=year))
    logger.info(f'Feching dataset of {name}')

    if os.path.isfile(os.path.join(data_folder, name)):
        frame = pd.read_excel(os.path.join(data_folder, name))
        logger.info(f'Read {name} from disk')
        if len(frame) == 0 and refetch_empty:
            logger.debug(f'The {name} frame is empty, try to fetch it again')
        else:
            return frame

    # Trigger backend service,
    # the single mode (action='one') does NOT work, and I do NOT know why,
    # it seems a bug on their web-site.
    url = r"http://data.sheshiyuanyi.com/WeatherData/php/downloadWeatherData.php"
    Params = dict(
        action='more',
        index='air_temperature',
        month='0',
        staNum=f'{ID}-{ID}',
        subIndex='avg_tem',
        year=f'{year}',
    )
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    response = requests.get(url=url, params=Params, headers=Headers)
    logger.debug(
        f'Query response is {response.text}, make sure it seems fine.')

    # Download excel,
    # it seems the backend is fast enough on preparing the data,
    # so there are NOT necessary to put some delay ^_^.
    try:
        url = template_url.format(**dict(ID=ID, year=year))
        frame = pd.read_excel(url)
    except Exception:
        traceback.print_exc()
        logger.error(f'Can not fetch {name} from website, please check it')
        return None

    frame.columns = ['ID', 'Year', 'Month', 'Day', 'Temp']
    logger.info(f'Fetched {name} from website')

    frame.to_excel(os.path.join(data_folder, name))
    logger.info(f'Wrote {name} to Excel file on the disk')

    return frame


# %%
for year in [2015, 2016, 2017]:
    for ID in tqdm(stations['ID']):
        fetch_data(ID, year)

# %%
