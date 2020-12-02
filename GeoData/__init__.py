import configparser
import logging
import os
import sys


def beside(name, this=__file__):
    # Get path of [name] beside __file__
    return os.path.join(os.path.dirname(this), name)


config = configparser.ConfigParser()
config.read(beside('setting.ini'))


logger = logging.Logger('GeoProject', level=logging.DEBUG)
for handler, formatter in zip([logging.StreamHandler(sys.stdout),
                               logging.FileHandler('logging.log')],
                              [logging.Formatter('%(filename)s %(levelname)s %(message)s'),
                               logging.Formatter('%(asctime)s %(name)s %(filename)s %(levelname)s %(message)s')]):
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.info('info')
logger.debug('debug')
logger.warning('warning')
logger.error('error')
logger.fatal('fatal')
