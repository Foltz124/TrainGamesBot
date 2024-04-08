import asyncio
import discord
import logging
import os

from systemd.journal import JournalHandler
from discord.ext import commands

class DiscordBot(commands.Bot):
    
    def __init__(self, guild_id, log_level):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents = intents, application_id=guild_id)

        self.logger = logging.getLogger('Jounal Logger')
        self.logger.addHandler(JournalHandler())
        self.logger.setLevel(log_level)

    async def load_cogs(self, cogs):
        for cog in cogs:
            await self.load_extension(f'cogs.{cog}')

    def run(self, token):
        super().start(token=token)

