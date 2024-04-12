import discord

from discord.ext import commands
from discord import app_commands

class UtilitiesCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.info('Utilities cog loaded')

    @commands.command(hidden = True)
    @commands.has_permissions(administrator = True)
    async def sync(self, ctx):
        guid = ctx.guild 
        ctx.bot.tree.copy_global_to(guild=guid)
        fmt = await ctx.bot.tree.sync(guild=guid)
        await ctx.send(f"synced {len(fmt)}")

    @app_commands.command(name = 'load', description = 'Load cog')
    async def load_cog(self, interaction, cog: str):
        message = "Successfully loaded " + cog + "."
        try:
            await self.bot.load_extension(f"cogs.{cog.lower()}") 
        except commands.ExtensionAlreadyLoaded as e:
            message = cog + " is already loaded." 
        await interaction.response.send_message(message)

    @app_commands.command(name = 'unload', description = 'Unload cog')
    async def unload_cog(self, interaction, cog: str):
        message = "Successfully unloaded " + cog + "."
        try:
            await self.bot.unload_extension(f"cogs.{cog.lower()}") 
        except commands.ExtensionNotLoaded as e:
            message = "Could not unload " + cog + "." 
        await interaction.response.send_message(message)

    @app_commands.command(name = 'reload', description = 'Reload cog')
    async def reload_cog(self, interaction, cog: str):
        message = "Successfully reloaded " + cog + "."
        try:
            await self.bot.reload_extension(f"cogs.{cog.lower()}") 
        except commands.ExtensionNotLoaded as e:
            message = "Could not reload " + cog + ". It is not currently loaded." 
        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(UtilitiesCog(bot))
