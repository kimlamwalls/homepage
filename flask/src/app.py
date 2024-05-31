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

    logging.debug(f"Getting posts from directory: {posts_dir}")

    for filepath in glob.glob(os.path.join(posts_dir, "*.md")):
        with open(filepath, 'r') as file:
            fileContent = file.read()
            md = markdown2.markdown(fileContent, extras=["metadata"])
            post = {
                'title': md.metadata.get('title', 'No title'),
                'date': md.metadata.get('date', 'No date'),
                'content': md,
                'slug': os.path.basename(filepath).split('.')[0]
            }
            posts.append(post)
            logging.debug(f"Post: {post}")
    return posts


@app.route('/')
def index():
    logging.debug("Index page")
    posts = get_posts()
    return render_template('index.html', posts=posts)


@app.route('/post/<post_slug>/')
def post(post_slug):
    posts = get_posts()
    post = next((post for post in posts if post['slug'] == post_slug), None)
    if post:
        return render_template('post.html', post=post)
    else:
        logging.debug(f"Post with slug {post_slug} not found, redirecting to index")
        return redirect(url_for('index'))


if __name__ == '__main__':
    logging.debug("Running app, Logging is working")
    app.run(debug=True)
