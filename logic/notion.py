import discord
from util.notion import NotionClient
import util.discord_label as label
import util.notion_pagetracker as tracker
import bot_config

async def send_photo_request(ctx, post):
  
  if tracker.post_tracker.has_page(post['id']):
    return
      
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


async def find_requesting_asset_posts():
  posts = NotionClient.get_requesting_posts()
  return posts

def mark_as_acknowledged(page_id):
  tracker.post_tracker.update_page(page_id, acknowledged=True)
  NotionClient.mark_as_acknowledged(page_id)

def mark_as_complete(page_id):
    tracker.post_tracker.update_page(page_id, completed=True)
    NotionClient.mark_as_complete(page_id)

async def mark_as_deferred(page_id, ctx = None):
    tracker.post_tracker.update_page(page_id, deferred=True)
    NotionClient.mark_as_acknowledged(page_id)
    if ctx:
        await ctx.send(f"<@{bot_config.DISCORD_ADMIN_ID}> deal with this")

async def read_tracker(page_id, ctx, **kwargs):
    flag = 0
    for key, value in kwargs.items():
        if key in label.labels:
            if value:
                flag |= label.flags[key]
    # print(f"Flag: {flag}")

    if flag & label.flags['complete']:
        mark_as_complete(page_id)
    elif flag & label.flags['deferred']:
        await mark_as_deferred(page_id, ctx)
    elif flag & label.flags['acknowledged']:
        mark_as_acknowledged(page_id)
    