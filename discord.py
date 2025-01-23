import os
import load_dotenv
import requests


load_dotenv.load_dotenv() # Load environment variables from .env file
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')

# requests.post(DISCORD_WEBHOOK, json={