from flask import render_template
from .. import db
from ..models import Post, Subscriber

from . import main

@main.route('/about', methods=['GET'])
@main.route('/', methods=['GET'])
def index():
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@main.route('/writing', methods=['GET'])
def writing():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('writing.html', posts=posts)
