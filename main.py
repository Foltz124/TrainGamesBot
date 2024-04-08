import asyncio
import settings

from bot import DiscordBot

if __name__ == '__main__':
    async def main():
        bot = DiscordBot(settings.GUILD_ID, settings.LOG_LEVEL)

        @bot.event
        async def on_ready():
            self.logger('Bot online')

        await bot.load_cogs([ 'error', 'utilities' ])
        await bot.start(settings.TOKEN)

asyncio.run(main())

