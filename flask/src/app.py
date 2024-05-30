from flask import Flask, render_template, url_for, redirect
import os
import markdown2
import glob

app = Flask(__name__)

def get_posts():
    posts = []
    for filepath in glob.glob("src/pages/posts/*.md"):
        with open(filepath, 'r') as file:
            content = file.read()
            md = markdown2.markdown(content, extras=["metadata"])
            post = {
                'title': md.metadata.get('title', 'No title'),
                'date': md.metadata.get('date', 'No date'),
                'content': md,
                'slug': os.path.basename(filepath).split('.')[0]
            }
            posts.append(post)
    return posts

@app.route('/')
def index():
    posts = get_posts()
    divs = [f"Div Content {i}" for i in range(1, 4)]  # Example dynamic content
    return render_template('index.html', posts=posts, divs=divs)

@app.route('/post/<post_slug>')
def post(post_slug):
    posts = get_posts()
    post = next((post for post in posts if post['slug'] == post_slug), None)
    if post:
        return render_template('post.html', post=post)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
