from discord.ext import commands
import bot_config
import discord
import util.discord_label as label
import util.notion_pagetracker as tracker
import logic.notion as notion_logic
import datetime

class NotionBot(commands.Bot):
    async def on_message(self, message):
        # if message.channel.id != int(bot_config.CHANNEL_ID):
        #   return
        if message.author.bot:
            return
        print(f"Message from {message.author}: {message.content}")
        await self.process_commands(message)

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')
        print('------')
        channel_id = bot_config.CHANNEL_ID  # Replace with your actual channel ID
        channel = self.get_channel(channel_id)
        
        print(f"Channel: {channel}")
        # Check existing requests
        if channel:
            try:
                # Fetch recent messages (adjust limit as needed)
                async for message in channel.history(limit=100):
                    if not message.author.id == self.user.id:
                        continue
                    if not message.embeds:
                        continue
                    
                    # Display message content
                    embed = message.embeds[0]

                    page_id = embed.footer.text.split(':')[-1].strip()
                    
                    # Display reactions
                    updated_track = {}
                    for reaction in message.reactions:
                        if label.reaction_map.get(reaction.emoji):
                            updated_track[label.reaction_map.get(reaction.emoji)] = reaction.count > 1
                    
                    print(f"Page ID: {page_id}, Updated track: {updated_track}")
                    tracker.post_tracker.update_page(page_id, **updated_track)
                    new_track = tracker.post_tracker.get_page(page_id)
                    await notion_logic.read_tracker(page_id, channel, **new_track)


                    # if the message is 7 days old, delete it
                    if message.created_at < discord.utils.utcnow() - datetime.timedelta(days=7):
                        if new_track.get('completed', False):
                            await message.delete()


            except discord.errors.Forbidden:
                print("No permission to read message history")
            except Exception as e:
                print(f"Error checking messages: {e}")

        # Check for new requests
        newposts = await notion_logic.find_requesting_asset_posts()
        for post in newposts:
            if not tracker.post_tracker.has_page(post['id']):
                await notion_logic.send_photo_request(channel, post)

    async def setup_hook(self):
        await self.load_extension('cogs.notion_commands')
        return await super().setup_hook()