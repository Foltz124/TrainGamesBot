import asyncio
import discord
import os

from discord.ext import commands
from cogs.error import ExceptionHandlingCog
from cogs.utilities import UtilitiesCog
from cogs.train_game import TrainGameCog

def run(debug: bool, token, guild_id):
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents = intents, application_id=guild_id)

    @bot.event
    async def on_ready():
        print('Bot online')

    async def load():
        await bot.add_cog(TrainGameCog(bot))
        await bot.add_cog(ExceptionHandlingCog(bot))
        await bot.add_cog(UtilitiesCog(bot))

    async def start():
        await load()
        await bot.start(token)

    asyncio.run(start())
