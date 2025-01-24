import os
import load_dotenv

load_dotenv.load_dotenv() # Load environment variables from .env file
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_COMMAND_PREFIX = os.getenv('DISCORD_COMMAND_PREFIX')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
DISCORD_ADMIN_ID = int(os.getenv('DISCORD_ADMIN_ID'))


NOTION_TOKEN = os.getenv('NOTION_API_KEY')
DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

