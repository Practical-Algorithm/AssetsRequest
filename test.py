from util.notion import Notion
import bot_config

notion = Notion(token=bot_config.NOTION_TOKEN, 
                database_id=bot_config.DATABASE_ID)

posts = notion.get_requesting_posts()

for post in posts:
    print(post['title'])
    page = notion.read_page(post['id'])
    print(page)