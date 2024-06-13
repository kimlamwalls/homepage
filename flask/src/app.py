import logging
from flask import Flask, render_template, url_for, redirect
import os
import markdown2
import glob

app = Flask(__name__, static_url_path='/static')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def get_posts():
    posts = []
    base_dir = os.path.dirname(__file__)
    posts_dir = os.path.join(base_dir, 'pages', 'posts')
    #logging.debug(f"Getting posts from directory: {posts_dir}")
    for filepath in glob.glob(os.path.join(posts_dir, "*.md")):
        with open(filepath, 'r') as file:
            fileContent = file.read()
            md = markdown2.markdown(fileContent, extras=["metadata"])
            post = {
                'title': md.metadata.get('title', 'No title'),
                'date': md.metadata.get('date', 'No date'),
                'image': md.metadata.get('image', None),
                'roles': md.metadata.get('roles', None),
                'card_image': md.metadata.get('card_image', None),
                'card_image_alt': md.metadata.get('card_image_alt', None),
                'card_video': md.metadata.get('card_video', None),
                'description': md.metadata.get('description', 'No description'),
                'category': md.metadata.get('category', None),
                'content': md,
                'slug': os.path.basename(filepath).split('.')[0]
            }
            posts.append(post)
            #logging.debug(f"Post: {post}")
    return posts


def get_categories(posts):
    categories = {post['category'] for post in posts if post['category']}
    category_biases = {
        'Design': 1,
    }
    # remove biased categores from categories list and place them in their own list
    biased_categories = [category for category in categories if category in category_biases]
    categories = [category for category in categories if category not in category_biases]
    sorted_categories = sorted(categories)
    sorted_biased_categories = sorted(biased_categories, key=lambda x: category_biases[x])
    # add sorted biased categories to the end of sorted categories
    return sorted_categories + sorted_biased_categories

@app.route('/')
def index():
    logging.debug("Index page")
    posts = get_posts()
    categories = get_categories(posts)
    logging.debug(f"Categories: {categories}")
    return render_template('index.html', posts=posts, categories=categories)


@app.route('/post/<post_slug>/')
def post(post_slug):
    posts = get_posts()
    categories = get_categories(posts)
    post = next((post for post in posts if post['slug'] == post_slug), None)
    if post:
        return render_template('post.html', post=post, categories=categories)
    else:
        logging.debug(f"Post with slug {post_slug} not found, redirecting to index")
        return redirect(url_for('index'))


if __name__ == '__main__':
    logging.debug("Running app, Logging is working")
    app.run(debug=True)
