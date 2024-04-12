import discord
import modules.game_data as GD
import modules.player as PL
import settings
import sqlite3
import time

from datetime import datetime
from discord import app_commands
from discord.ext import commands, tasks

LINE_SEPARATOR = '\n'
BASE_URL = 'https://18xx.games/game/'

def _get_turn_embed(game):
    embed = discord.Embed(color=discord.Color.dark_teal(), url= BASE_URL + str(game.id),
            title = game.title)
    embed.add_field(name = 'Description', value = game.description)
    embed.add_field(name = 'Turn', value = game.turn, inline = True)
    embed.add_field(name = 'Round', value = game.round, inline = True)
    return embed

def _get_current_games(games):
    embed = discord.Embed(color=discord.Color.dark_teal(), title = 'Current Games')
    title_string = LINE_SEPARATOR.join(f'[{game.title}]({BASE_URL}{str(game.id)})' for game in games)
    turn_string = LINE_SEPARATOR.join(str(game.turn) for game in games)
    round_string = LINE_SEPARATOR.join(game.round for game in games)
    embed.add_field(name = "Title", value = title_string)
    embed.add_field(name = "Turn", value = turn_string)
    embed.add_field(name = "Round", value = round_string)
    return embed

class TrainGameCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = sqlite3.connect(settings.DATABASE_FILE)

    @commands.Cog.listener()
    async def on_ready(self):
        self.update_game_states.start()
        self.bot.info('Train game cog loaded')

    async def cog_unload():
        self.update_game_states.cancel()
        self.database.close()
        self.bot.info('Train game cog unloaded')

    @app_commands.command(name = 'track_game', description = 'Track a game on 18xx.games')
    async def track_game(self, interaction, game_id: int):
        result = GD.get_game_data(game_id)
        if result is not None and GD.save_game_data(self.database, result):
            await interaction.response.send_message("Successfully tracked game.")
        else:
            await interaction.response.send_message('Failed to track game. Please make sure provided ID is correct.', ephemeral = True)

    @app_commands.command(name = 'sync_player', description = 'Adds player to the database. Used in auto updates')
    async def sync_player(self, interaction, player_id: int):
        if PL.save_player(self.database, player_id, interaction.user.id): 
            await interaction.response.send_message("Successfully synced user.")
        else:
            await interaction.response.send_message('Failed to sync user.', ephemeral = True)

    @app_commands.command(name = 'unsync_player', description = 'Removes player from the database. Used in auto updates')
    async def unsync_player(self, interaction, player_id: int):
        if PL.delete_player(self.database, player_id): 
            await interaction.response.send_message("Successfully unsynced user.")
        else:
            await interaction.response.send_message('Failed to unsync user.', ephemeral = True)

    @app_commands.command(name = 'current_games', description = 'Lists current games.')
    async def current_games(self, interaction):
        tracked_games = GD.get_tracked_games(self.database)
        if len(tracked_games) > 0: 
            await interaction.response.send_message(embed = _get_current_games(tracked_games))
        elif tracked_games is None: 
            await interaction.response.send_message('Unable to get tracked games.', ephemeral = True)
        else:
            await interaction.response.send_message('I am not currently tracking any games.')

    @tasks.loop(seconds=5)
    async def update_game_states(self):
        try:
            tracked_games = GD.get_tracked_games(self.database)
            for tracked_game in tracked_games:
                pulled_game_data = GD.get_game_data(tracked_game.id)
                if pulled_game_data is None:
                    continue
                hour_check = (time.time() - pulled_game_data.updated_at) % 3600
                if pulled_game.current_player != tracked_game.current_player or hour_check == 0:
                    self.bot.debug(f'User: {pulled_game.current_player}, Hour Check: {hour_check}')
                    GD.save_game_data(self.database, pulled_game)
                    user_id = PL.get_discord_id(self.database, pulled_game.current_player)
                    if user_id is None:
                        continue
                    user = await self.bot.fetch_user(user_id)
                    await user.send(embed = _get_turn_embed(pulled_game))
        except Exception as e:
            self.bot.error(e.reason)

async def setup(bot):
    await bot.add_cog(TrainGameCog(bot))
