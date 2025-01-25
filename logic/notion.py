import discord
from util.notion import NotionClient
import util.discord_label as label
import util.notion_pagetracker as tracker


async def send_photo_request(ctx, post):
  page_id = post['id']
  page_title = post['title']

  print("Sending photo request for post: ", post['title'])
  page, error = NotionClient.read_page(page_id)

  photo_request = None
  if error:
      photo_request = ["Error reading page, please manually check the page"]                
  else:
      photo_request = NotionClient.extract_photo_request(page)

  if len(photo_request) == 0:
      NotionClient.mark_as_complete(page_id)
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
  await message.add_reaction(label.acknowledge)  # ok hand emoji
  await message.add_reaction(label.complete)  # relaxed
  await message.add_reaction(label.defer)  # mobile phone emoji

  tracker.post_tracker.add_page(page_id)


async def find_requesting_asset_posts(ctx):
  posts = NotionClient.get_requesting_posts()
  if len(posts) == 0:
      await ctx.send("No posts found")
      return
  for post in posts:
      await send_photo_request(ctx, post)