import discord
import logging
import os
import pathlib

TOKEN =  os.environ['BOT_TOKEN']
GUILD_ID = os.environ['BOT_GUILD']

BASE_DIR = pathlib.Path(__file__).parent

DATABASE_FILE = BASE_DIR / 'sql' / 'train_games.db'

LOG_LEVEL = logging.INFO

LOG_FILE_PATH = './train_game.log'
