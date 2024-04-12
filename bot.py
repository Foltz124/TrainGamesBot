import asyncio
import discord
import logging
import os

from discord.ext import commands

class DiscordBot(commands.Bot):
    
    def __init__(self, guild_id, log_level, log_file_path):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents = intents, application_id=guild_id)

        handler = logging.FileHandler(filename=log_file_path, encoding='utf-8', mode='w')
        self.logger = logging.getLogger('Train Game Logger')
        self.logger.addHandler(handler)
        self.logger.setLevel(log_level)

    def debug(message: str):
        self.logger.debug(message)

    def info(message: str):
        self.logger.info(message)

    def warning(message: str):
        self.logger.warning(message)
        
    def error(message: str):
        self.logger.error(message)

    def critical(message: str):
        self.logger.critical(message)

    async def load_cogs(self, cogs):
        for cog in cogs:
            await self.load_extension(f'cogs.{cog}')

    def run(self, token):
        super().start(token=token)

