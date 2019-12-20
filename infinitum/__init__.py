#! /bin/python3
import logging

from .core.config import Config, sdump_config


LOG_FORMAT = '%(asctime)s [%(levelname)s] [%(module)s]: %(message)s'
LOG_DATEFMT = '%m/%d/%Y %I:%M:%S %p'


def setup(config_path) -> Config:
    config = Config(config_path)
    if config.debug:
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=LOG_DATEFMT)
        logging.debug('Set loglevel to DEBUG')
        config_dump = sdump_config(config)
        logging.debug(f'Dump of config loaded:\n{config_dump}')
    else:
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATEFMT)
        logging.info('Set loglevel to INFO')
    return config

