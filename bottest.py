import notion

posts = notion.get_posts()


post = posts[0]
print(notion.read_page(post['id']))