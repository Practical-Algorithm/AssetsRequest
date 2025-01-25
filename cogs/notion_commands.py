from discord.ext import commands
import bot_config
import util.discord_label as label
import logic.notion as notion_logic

class NotionCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='check')
    async def manual_check(self, ctx):
        # Remove the command message
        await ctx.message.delete()

        print("Checking for new requests")
        posts = await notion_logic.find_requesting_asset_posts()
        if len(posts) == 0:
            await ctx.send("No posts found")
            return
        for post in posts:
            await notion_logic.send_photo_request(ctx, post)

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
            if reaction.emoji == label.acknowledge:
                """Content team has acknowledged the request"""
                notion_logic.mark_as_acknowledged(page_id)
            elif reaction.emoji == label.complete:
                """Mark the note as complete"""
                notion_logic.mark_as_complete(page_id)
            elif reaction.emoji == label.defer:
                """Contact @Phon1209 to add more components instead"""
                notion_logic.mark_as_deferred(page_id, ctx)

async def setup(bot):
    await bot.add_cog(NotionCommands(bot))