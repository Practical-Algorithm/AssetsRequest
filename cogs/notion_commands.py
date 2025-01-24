import discord
from discord.ext import commands
import bot_config
from util.notion import Notion

class NotionCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notion = Notion(token=bot_config.NOTION_TOKEN, database_id=bot_config.DATABASE_ID)

    async def send_photo_request(self, ctx, post):
        page_id = post['id']
        page_title = post['title']

        print("Sending photo request for post: ", post['title'])
        page, error = self.notion.read_page(page_id)

        photo_request = None
        if error:
            photo_request = ["Error reading page, please manually check the page"]                
        else:
            photo_request = self.notion.extract_photo_request(page)

        if len(photo_request) == 0:
            self.notion.mark_as_complete(page_id)
            return
        
        # convert list to numbered list in markdown
        photo_request = [f"{i+1}. {line}" for i, line in enumerate(photo_request)]

        photo_request = '\n'.join(photo_request)
        # escape markdown formatting
        photo_request = photo_request.replace('*', '\*')
        photo_request = photo_request.replace('_', '\_')
        photo_request = photo_request.replace('~', '\~')
        photo_request = photo_request.replace('`', '\`')
        photo_request = photo_request.replace('|', '\|')

        photo_request += f"\n\n[Link to Notion page]({post['link']})"


        embed = discord.Embed(title=f"New photo request from \"{page_title}\"", color=0x2D6C1E, description=photo_request)
        embed.set_footer(text=f"metadata: {page_id}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('👌')  # ok hand emoji
        await message.add_reaction('☺️')  # relaxed
        await message.add_reaction('📲')


    @commands.command(name='check')
    async def find_requesting_asset_posts(self, ctx):
        posts = self.notion.get_requesting_posts()
        if len(posts) == 0:
            await ctx.send("No posts found")
            return
        for post in posts:
            await self.send_photo_request(ctx, post)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        # Ignore bot reaction
        if user == self.bot.user:
            return
        
        page_id = None
        print(user)
        if reaction.message.embeds:
            footer_text = reaction.message.embeds[0].footer.text
            if footer_text.startswith('metadata:'):
                page_id = footer_text.split(':')[1].strip()

        if page_id:
            if reaction.emoji == '👌':
                """Content team has acknowledged the request"""
                print(f"Ack Page ID: \'{page_id}\'")
                self.notion.mark_as_acknowledged(page_id)
            elif reaction.emoji == '☺️':
                """Mark the note as complete"""
                print(f"com Page ID: \'{page_id}\'")

                self.notion.mark_as_complete(page_id)
            elif reaction.emoji == '📲':
                """Contact @Phon1209 to add more components instead"""
                await reaction.message.channel.send(f"<@{bot_config.DISCORD_ADMIN_ID}> deal with this")

async def setup(bot):
    await bot.add_cog(NotionCommands(bot))