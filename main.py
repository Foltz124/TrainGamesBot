import argparse
import bot 
import settings

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-d', '--debug', action='store_true',
        help='Run the application in debug mode.')

if __name__ == '__main__':
    bot.run(arg_parser.parse_args().debug, settings.TOKEN, settings.GUILD_ID)
