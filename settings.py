import discord
import os
import pathlib

TOKEN =  os.environ["TRAIN_BOT_TOKEN"]
GUILD_ID = os.environ["TRAIN_BOT_GUILD"]

BASE_DIR = pathlib.Path(__file__).parent

DATABASE_FILE = BASE_DIR / "sql" / "train_games.db"
