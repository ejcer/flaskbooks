from datetime import datetime
from . import db

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.String(64), index=True)

    def __init__(self, body, timestamp, author_id):
        self.body = body
        self.timestamp = timestamp
        self.author_id = author_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Subscriber(db.Model):
    __tablename__= 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<id {}>'.format(self.id)
