import discord
import logging
import os
import pathlib

from logging import config


TOKEN =  os.environ["TRAIN_BOT_TOKEN"]
GUILD_ID = discord.Object(os.environ["TRAIN_BOT_GUILD"])

BASE_DIR = pathlib.Path(__file__).parent

DATABASE_FILE = BASE_DIR / "sql" / "train_games.db"

LOGGING_CONFIG = {
    'version': 1,
    'disabled_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s'
        },
        'standard': {
            'format': '%(levelname)-10s - %(name)-15s : %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/bgg_bot.log',
            'formatter': 'verbose',
            'mode': 'w',
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/debug_bgg_bot.log',
            'formatter': 'verbose',
            'mode': 'w',
        },
    },
    'loggers': {
        'debug': {
            'handlers': ['console', 'debug_file'],
            'level': 'DEBUG',
            'propogate': True,
        },
        'standard': {
            'handlers': ['file'],
            'level': 'INFO',
            'propogate': True,
        }
    }
}

config.dictConfig(LOGGING_CONFIG)
