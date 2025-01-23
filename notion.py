import os
import load_dotenv
from notion_client import Client, APIErrorCode, APIResponseError
import json
import logging

load_dotenv.load_dotenv() # Load environment variables from .env file
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
notion = Client(auth=NOTION_API_KEY)
# notion = Client(auth=NOTION_API_KEY, log_level=logging.DEBUG)

def extract_notion_data(obj: dict) -> dict:
  properties = obj.get("properties", {})
  id = obj.get("id")
  link = obj.get("url")
  title = properties.get("Title").get("title")[0].get("plain_text")
  status = properties.get("Status").get("select", None)
  status = status.get("name") if status else None

  return {
    "id": id,
    "link": link,
    "title": title,
    "status": status or "Not Started"
  }

# def extract_notion_page_data(obj: dict) -> dict:


def get_posts(limit: int = 10):
  posts = notion.databases.query(database_id=NOTION_DATABASE_ID)
  posts = json.loads(json.dumps(posts))
  posts = posts['results']

  return [extract_notion_data(post) for post in posts]

def read_page(page_id: str):
  page = notion.blocks.children.list(block_id=page_id)

  return page

# def change_page_status(page_id: str, new_status: str):
#   page = notion.pages.update(
#     page_id=page_id,
#     properties={
#       "Status": {
#         "select": {
#           "name": new_status
#         }
#       }
#     }
#   )

#   return page