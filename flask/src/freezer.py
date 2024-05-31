from flask_frozen import Freezer
from app import app, get_posts

freezer = Freezer(app)

@freezer.register_generator
def post():
    for post in get_posts():
        yield {'post_slug': post['slug']}

if __name__ == '__main__':
    freezer.freeze()