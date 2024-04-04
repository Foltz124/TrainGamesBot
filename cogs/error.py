import discord
from discord.ext import commands
from discord import app_commands

# Cog to ensure that all unhandled exceptions are caught,
# and users are alerted. Only a few generic issues should be 
# addressed here. This is mostly to catch coding errors that
# would otherwise be hidden by the bot.
class ExceptionHandlingCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.tree.error(coro = self.__dispatch_to_app_command_handler)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Exception handling cog loaded')

    async def __dispatch_to_app_command_handler(self, interaction, error):
        self.bot.dispatch('app_command_error', interaction, error)

    @commands.Cog.listener('on_app_command_error')
    async def get_app_command_errror(self, interaction, error):
        message = "Unable to process request. Please alert the bot owner."
        if isinstance(error, commands.MissingRequiredArgument):
            message = "You are missing a required argument, please try again."
        print(error)
        await interaction.response.send_message(message, ephemeral = True)

async def setup(bot):
    await bot.add_cog(ExceptionHandlingCog(bot))
