from flask import render_template, session, redirect, url_for, current_app, request
from .. import db
from ..models import Post, Subscriber
from forms import ContactForm, LoginForm, PostForm
from ..email import send_email
from . import main
import webbrowser
import functools


### Auth Routes ###

def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('.login', next=request.path))
    return inner

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        app = current_app._get_current_object()
        password = form.password.data
        if password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session.permanent = True
            return redirect(url_for('.index'))
    return render_template('login.html', form=form)


@main.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('.login'))
    return render_template('logout.html')


### Main Static Routes ###

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        app = current_app._get_current_object()
        send_email(app.config['ADMIN'], \
            'Assistance Request [edwardmcenrue.com]', \
            'email/contact_req', \
            name=form.name.data, \
            email=form.email.data, \
            contact_req=form.contact_req.data)
        return redirect(url_for('.contact'))
    return render_template('contact.html', form=form)


### Main Dynamic Routes ###

@main.route('/articles', methods=['GET'])
def articles():
    posts = Post.public().order_by(Post.timestamp.desc()).all()
    return render_template('articles.html', posts=posts)

@main.route('/drafts/')
@login_required
def drafts():
    posts = Post.drafts().order_by(Post.timestamp.desc()).all()
    return render_template('articles.html', posts=posts)

@main.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=request.form['title'],
            body=request.form['body'],
            published=request.form.get('published') or False,
            )
        db.session.add(post)
        if post.published:
            return redirect(url_for('.detail', slug=post.slug))
        else:
            return redirect(url_for('.edit', slug=post.slug))
    return render_template('create.html', form=form)

@main.route('/<slug>/')
def detail(slug):
    if session.get('logged_in'):
        post = Post.query.filter_by(slug=slug).first()
    else:
        post = Post.public().filter_by(slug=slug).first()
    if post is not None:
        return render_template('detail.html', post=post)
    else:
        return render_template('404.html'), 404

@main.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit(slug):
    form = PostForm()
    post = Post.query.filter_by(slug=slug).first()

    if post:
        if form.validate_on_submit():
            if request.form.get('title') and request.form.get('body'):
                post.title = form.title.data
                post.body = form.body.data
                post.published = form.published.data or False
                post.update_slug()
                if post.published:
                    return redirect(url_for('.detail', slug=post.slug))
                else:
                    return redirect(url_for('.edit', slug=post.slug))
        return render_template('edit.html', post=post, form=form)
    else:
        return render_template('404.html'), 404
