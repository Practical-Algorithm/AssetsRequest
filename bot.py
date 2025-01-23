from discord.ext import commands
import bot_config

class NotionBot(commands.Bot):
    async def on_message(self, message):
        # if message.channel.id != int(bot_config.CHANNEL_ID):
        #   return
        print(f"Message from {message.author}: {message.content}")
        await self.process_commands(message)

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')
        print('------')

    async def setup_hook(self):
        await self.load_extension('cogs.notion_commands')
        return await super().setup_hook()