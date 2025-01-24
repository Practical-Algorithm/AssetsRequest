from notion_client import Client
import json
from notion2md.exporter.block import MarkdownExporter, StringExporter

class Notion():
  def __init__(self, token, database_id) -> None:
    self.client = Client(auth=token)
    self.token = token
    self.database_id = database_id

  def extract_page_data(self, obj: dict) -> dict:
      properties = obj.get("properties", {})
      id = obj.get("id")
      link = obj.get("url")
      title = properties.get("Title").get("title")[0].get("plain_text")
      status = properties.get("Status").get("status").get("name")

      return {
        "id": id,
        "link": link,
        "title": title,
        "status": status
      }

  def get_requesting_posts(self, limit: int = 10):
    posts = self.client.databases.query(
      database_id=self.database_id,
      filter={
        "property": "Status",
        "status": {
          "equals": "Assets: Requesting",
      }
    })
    posts = json.loads(json.dumps(posts))
    posts = posts["results"]

    return [self.extract_page_data(post) for post in posts]
  
  def get_acknowledged_posts(self, limit: int = 10):
    posts = self.client.databases.query(
      database_id=self.database_id,
      filter={
        "property": "Status",
        "status": {
          "equals": "Assets: Requesting",
      }
    })
    posts = json.loads(json.dumps(posts))
    posts = posts["results"]

    return [self.extract_page_data(post) for post in posts]

  def read_page(self, page_id: str) -> tuple[str, Exception]:
    try:
      page = StringExporter(block_id=page_id, token=self.token).export()
      return page, None
    except Exception as e:
      return None, e

  def extract_photo_request(self, page: str) -> list[str]:
    photo_request = [line for line in page.split('\n') if '—' in line]
    return photo_request
  
  def mark_as_acknowledged(self, page_id: str):
    self.client.pages.update(
      page_id=page_id,
      properties={
        "Status": {
          "status": {
            "name": "Assets: Acknowledged"
          }
        }
      }
    )

  def mark_as_complete(self, page_id: str):
    self.client.pages.update(
      page_id=page_id,
      properties={
        "Status": {
          "status": {
            "name": "Completed"
          }
        }
      }
    )

  def export_page(self, page_id: str, filename: str):
    MarkdownExporter(block_id=page_id, token=self.token).export(filename=filename)