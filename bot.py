from discord.ext import commands
import bot_config
import discord
import util.discord_label as label
import util.notion_pagetracker as tracker

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
                    
                    tracker.post_tracker.update_page(page_id, **updated_track)

            except discord.errors.Forbidden:
                print("No permission to read message history")
            except Exception as e:
                print(f"Error checking messages: {e}")

    async def setup_hook(self):
        await self.load_extension('cogs.notion_commands')
        return await super().setup_hook()