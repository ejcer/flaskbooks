from datetime import datetime
from flask import current_app, Markup
from . import db
import re
from markdown import markdown

from markdown.extensions.extra import ExtraExtension
# from markdown.extensions.codehilite import CodeHiLiteExtension
from micawber import bootstrap_basic, parse_html
from micawber.cache import Cache as OEmbedCache

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)
    body = db.Column(db.Text)
    published = db.Column(db.Boolean, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @property
    def html_content(self):
        app = current_app._get_current_object()
        # hilite = CodeHiLiteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()
        #TODO why can I not add CodeHiLiteExtension????
        # markdown_content = markdown(self.body, extensions=[hilite, extras])
        markdown_content = markdown(self.body, extensions=[extras])
        oembed_providers = bootstrap_basic(OEmbedCache())
        oembed_content = parse_html(
            markdown_content,
            oembed_providers,
            urlize_all=True,
            maxwidth=app.config['SITE_WIDTH'])
        return Markup(oembed_content)

    def __init__(self, title, body, published, timestamp):
        self.title = title
        self.body = body
        self.published = published
        self.timestamp = timestamp

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)
        if self.slug is None:
            self.slug = re.sub('[^\w]+', '-', self.title.lower())

    def update_slug(self):
        self.slug = re.sub('[^\w]+', '-', self.title.lower())

    @classmethod
    def public(cls):
        return Post.query.filter_by(published = True)

    @classmethod
    def drafts(cls):
        return Post.query.filter_by(published = False)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Subscriber(db.Model):
    __tablename__= 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)

    # def __init__(self, email):
    #     self.email = email

    def __repr__(self):
        return '<id {}>'.format(self.id)
