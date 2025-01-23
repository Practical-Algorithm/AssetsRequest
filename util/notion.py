from notion_client import Client, APIErrorCode, APIResponseError
import json
from notion2md.exporter.block import MarkdownExporter, StringExporter
from bot_config import NOTION_API_KEY, NOTION_DATABASE_ID

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
def get_posts(limit: int = 10):
  posts = notion.databases.query(database_id=NOTION_DATABASE_ID)
  posts = json.loads(json.dumps(posts))
  posts = posts["results"]

  return [extract_notion_data(post) for post in posts]

def read_page(page_id: str) -> str:
  page = StringExporter(block_id=page_id, token=NOTION_API_KEY).export()
  return page

def extract_photo_request(page: str) -> list[str]:
  photo_request = [line for line in page.split('\n') if '—' in line]
  return photo_request
