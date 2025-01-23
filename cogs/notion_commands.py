from discord.ext import commands
from notion_client import Client
import bot_config
from util.notion import Notion

class NotionCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notion = Client(auth=bot_config.NOTION_TOKEN)

    @commands.command(name='update')
    async def ping(self, ctx):
        """remove the command message and send pong"""
        # await ctx.message.delete()
        await ctx.message.channel.send('Pong!')

async def setup(bot):
    await bot.add_cog(NotionCommands(bot))