import discord
import logging
from bot import NotionBot
import bot_config

def main():
    
    handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
    intents = discord.Intents.default()
    intents.message_content = True
    bot = NotionBot(
        command_prefix=bot_config.DISCORD_COMMAND_PREFIX, 
        intents=intents
    )
    bot.run(bot_config.DISCORD_TOKEN, log_handler=handler)

if __name__ == '__main__':
    main()