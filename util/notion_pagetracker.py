import json
import os
import util.discord_label as label

class NotionPageTracker:
    def __init__(self, db_path='notion_pages.json'):
        self.db_path = db_path
        self.load_database()

    def load_database(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                self.pages = json.load(f)
        else:
            self.pages = {}

    def save_database(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.pages, f, indent=4)

    def add_page(self, post_id, **kwargs):
        new_page = {}
        for key in label.labels:
            new_page[key] =  False
        for key, value in kwargs.items():
            if key in label.labels:
                new_page[key] = value
        self.pages[post_id] = new_page
        self.save_database()

    def update_page(self, post_id, **kwargs):
        if post_id not in self.pages:
            raise KeyError(f"Page {post_id} not found")
        
        for key, value in kwargs.items():
            if key in label.labels:
                self.pages[post_id][key] = value
        
        self.save_database()
    
    def has_page(self, post_id):
        return post_id in self.pages

    def get_page(self, post_id):
        return self.pages.get(post_id)

    def list_pages(self):
        return self.pages
    
    def has_call_admin(self, post_id):
        if post_id not in self.pages:
            raise KeyError(f"Page {post_id} not found")
        return self.pages[post_id].get('has_call_admin', False)

    def set_call_admin(self, post_id):
        if post_id not in self.pages:
            raise KeyError(f"Page {post_id} not found")
        self.pages[post_id]['has_call_admin'] = True
        self.save_database()

            

post_tracker = NotionPageTracker()